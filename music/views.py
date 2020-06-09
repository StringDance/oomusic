import math

import wordcloud
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from wordcloud import WordCloud
import pandas as pd
from comment.forms import CommentForm
from comment.models import Comment
from userprofile.models import LikesAndDislikes
from .models import Music, Album, Singer, Record, MusicTag
from django.core.paginator import Paginator


def index(request):
    popular_songs = Music.objects.order_by('-total_views')[:11]
    new_albums = Album.objects.order_by('-release_date')[:3]
    context = {'popular_songs':popular_songs,'new_albums':new_albums}
    return render(request,'music/index1.html',context)


def music_list(request):
    # 根据GET请求中查询条件,返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索,Q(music_name__icontains=search)是在模型的music_name字段查询，icontains是不区分大小写的包含。
            search_results = Music.objects.filter(
                Q(name__contains=search) |
                Q(singer__name__contains=search)|
                Q(album__name__contains=search)
            ).order_by('-total_views')
        else:
            search_results = Music.objects.filter(
                Q(name__contains=search) |
                Q(singer__name__contains=search)|
                Q(album__name__contains=search)
            )
    else:
        # 将 search 参数重置为空,如果若用户没有搜索操作，则search = request.GET.get('search')会使得search = None，
        search = ''
        if order == 'total_views':
            search_results = Music.objects.all().order_by('-total_views')
        else:
            search_results = Music.objects.all()
    # 每页显示 n 首歌曲
    paginator = Paginator(search_results, 12)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    music = paginator.get_page(page)
    # order告知模板下一页应该如何排序
    context = {'music': music, 'order': order}
    # render函数：载入模板，并返回context对象
    return render(request, 'music/music_list1.html', context)


def music_detail(request,id):
    # 获取当前歌曲信息
    music_info = Music.objects.get(id=id)
    # 获取当前歌曲评论信息(分页)
    # comment = Comment.objects.filter(music=id) # 原码
    comments_list = Comment.objects.filter(music=id)
    paginator = Paginator(comments_list,5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    comment_form = CommentForm()
    context = {
        'music_info': music_info,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'music/music-detail1.html', context)


def album_detail(request, album_id):
    # 当前专辑信息
    album_details = get_object_or_404(Album, pk=album_id)
    # 所有歌曲信息
    music = Music.objects.all()
    # 此歌手的所有专辑信息,注意 album 后有's'
    albums = Album.objects.filter(singer=album_details.singer)
    context = {'album_details': album_details, 'music':music,'albums':albums}
    return render(request, 'music/album-detail.html',context)


def music_play(request, id):
    if request.method == 'POST':
        user = request.user # request.user并不能获取到当前登录的用户id，于是报错
        # 先歌曲播放次数加一
        music = Music.objects.get(id=id)
        music.total_views = music.total_views + 1
        music.save(update_fields=['total_views'])
        # 已登录则记录，未登录则不记录
        if user.is_authenticated:
            music_obj = Music.objects.get(id=id)
            new_record = Record(user=user, music=music_obj)
            new_record.save()
        return redirect("music:music_list")
    else:
        return HttpResponse("仅接受post请求。")


def singer_detail(request,singer_id):
    # 此歌手的信息
    singer = Singer.objects.get(id=singer_id)
    # 此歌手的所有歌曲信息
    music = Music.objects.filter(singer=singer_id)
    # 此歌手的所有专辑信息,注意 album 后有's'
    albums = Album.objects.filter(singer=singer_id)
    context = {'singer': singer, 'music': music, 'albums': albums}
    return render(request,'music/singer-detail1.html', context)


def record_detail(request,user_id):
    # 显示最近 30条
    user_record = Record.objects.filter(user=user_id)[:30]
    # 因为播放记录不会展示对同一首歌在不同时间的播放记录的，
    # 本来应该去掉重复的歌曲，但下面这条语句报错说Music has no attribute 'split'。
    # 而distinct()在models里面是没问题的。
    # user_record = user_record.distinct(music)
    context = {'user_record': user_record}
    return render(request, 'music/record-detail1.html', context)


# 推荐页的播放
def music_play2(request, id):
    if request.method == 'POST':
        user = request.user
        music = Music.objects.get(id=id)
        music.total_views = music.total_views + 1
        music.save(update_fields=['total_views'])
        if user.is_authenticated:
            music_obj = Music.objects.get(id=id)
            new_record = Record(user=user, music=music_obj)
            new_record.save()
        return redirect('music:daily_recommendation',user.id)


# 歌曲详情页的播放
def music_play3(request, id):
    if request.method == 'POST':
        user = request.user
        music = Music.objects.get(id=id)
        music.total_views = music.total_views + 1
        music.save(update_fields=['total_views'])
        if user.is_authenticated:
            music_obj = Music.objects.get(id=id)
            new_record = Record(user=user, music=music_obj)
            new_record.save()
        return redirect('music:music_detail',id)


# 删除评论
@login_required(login_url='/userprofile/login/')
def comment_delete(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        music_id = comment.music_id
        # 验证删除者是否为评论者
        if request.user != comment.user:
            return HttpResponse("仅限评论者删除该评论。")
        comment.delete()
        return redirect("music:music_detail",music_id)
    else:
        return HttpResponse("仅允许post请求")


# 歌手详情页添加喜欢的歌手
@login_required(login_url='/userprofile/login/')
def follow(request,id):
    if request.method == 'POST':
        user = request.user
        singer = Singer.objects.get(id=id)
        # user_id中用下划线而不是点，可以直接 user
        likes_dislikes = LikesAndDislikes.objects.get(user_id=user)
        disliked_singer_list = []
        for s in likes_dislikes.singer_disliked.all():
            disliked_singer_list.append(s)
        liked_singer_list = []
        for s in likes_dislikes.singer_liked.all():
            liked_singer_list.append(s)
        # 如果该歌手不在此用户喜欢的歌手里
        if singer not in liked_singer_list:
            # 不知道怎么遍历这个likes_dislikes.singer_disliked.all()，就先用上面的笨方法代替
            # if singer not in likes_dislikes.singer_disliked.all().iterator():
            # disliked_singer_list是可以遍历的
            # 如果该歌手也不在此用户不喜欢的歌手里,则加入此歌曲对象
            if singer not in disliked_singer_list:
                likes_dislikes.singer_liked.add(singer)
                # 添加成功，返回歌手详情
                return redirect("music:singer_detail",id)
            else:
                return HttpResponse("您已将该歌手设置为不喜欢，不能再设置为喜欢！")
        else:
            return HttpResponse("您已添加歌手，请勿重复添加！")
    else:
        return HttpResponse("仅允许post请求")

# 在歌曲详情页拉黑（不喜欢）歌手
@login_required(login_url='/userprofile/login/')
def blacklist(request,id):
    if request.method == 'POST':
        user = request.user
        singer = Singer.objects.get(id=id)
        likes_dislikes = LikesAndDislikes.objects.get(user_id=user)
        disliked_singer_list = []
        for s in likes_dislikes.singer_disliked.all():
            disliked_singer_list.append(s)
        liked_singer_list = []
        for s in likes_dislikes.singer_liked.all():
            liked_singer_list.append(s)
        # 如果该歌手不在此用户不喜欢的歌手里
        if singer not in disliked_singer_list:
            # 也不在喜欢的歌手里
            if singer not in liked_singer_list:
                likes_dislikes.singer_disliked.add(singer)
                # 添加成功，返回歌手详情
                return redirect("music:singer_detail",id)
            else:
                return HttpResponse("您已将该歌手设置为喜欢，不能再设置为不喜欢！")
        else:
            return HttpResponse("您已添加歌手，请勿重复添加！")
    else:
        return HttpResponse("仅允许post请求")


# 歌曲详情页屏蔽（不喜欢）歌曲
@login_required(login_url='/userprofile/login/')
def shield(requset,id):
    if requset.method == 'POST':
        user = requset.user
        music = Music.objects.get(id=id)
        likes_dislikes = LikesAndDislikes.objects.get(user_id=user)
        disliked_songs_list = []
        for s in likes_dislikes.song_disliked.all():
            disliked_songs_list.append(s)
        # 如果该歌曲不在此用户不喜欢的歌曲里
        if music not in disliked_songs_list:
            likes_dislikes.song_disliked.add(music)
            return redirect("music:music_detail", id)
        else:
            return HttpResponse("您已经屏蔽该歌曲，请勿重复操作！")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/userprofile/login/')
def daily_recommendation(request,id):
    music_info = Music.objects.all()
    # 用户偏好信息
    likes_dislikes = LikesAndDislikes.objects.get(user_id=id)
    # 用户播放记录
    user_record = Record.objects.filter(user=id)
    # 喜欢的标签
    tag_liked_obj = likes_dislikes.tag_liked.all()
    # 不喜欢的标签
    tag_disliked_obj = likes_dislikes.tag_disliked.all()
    # 不喜欢的歌手
    singer_disliked_obj = likes_dislikes.singer_disliked.all()
    # 喜欢的歌手
    singer_liked_obj = likes_dislikes.singer_liked.all()
    # 不喜欢的歌曲
    song_disliked_obj = likes_dislikes.song_disliked.all()
    if tag_disliked_obj.count() == 0 or tag_liked_obj.count() == 0 or singer_liked_obj.count() == 0:
        if user_record.count() < 50 :
            return HttpResponse('您至少要在偏好信息中填写您喜欢、不喜欢的歌曲类型和喜欢的歌手且您当前听歌数据过少，系统无法推荐！')
    # 设置推荐歌曲的数目
    N = 30
    # 推荐列表
    list1 = recomm_algorithm1(user_record,tag_liked_obj,tag_disliked_obj,singer_disliked_obj,singer_liked_obj,song_disliked_obj,N/2)
    #list2 = recomm_alogrithm2(user_record, N/2)

    # 推荐列表生成后记得把数据存入数据库
    # 因为list只有music_id,所以再传入music_info方便前端展示歌曲其他信息
    context = {'list':list1,'music_info':music_info}
    return render(request,'music/daily-recommendation.html',context)


'''
推荐算法1：基于用户偏好信息进行推荐，解决推荐系统的冷启动问题。
输入：用户喜欢的标签，不喜欢的标签，不喜欢的歌手，喜欢的歌手，不喜欢的歌曲(注意，输入参数数据类型均为queryset类型)，产生推荐歌曲数目
思路：根据用户所填写的偏好信息，计算歌曲标签与用户喜欢的标签重合数 x 和歌曲标签与用户不喜欢的标签重合数 y,
    对每一首歌曲进行评分，若是喜欢的歌手的歌则 score = ln(1.3^x-y) * 1.4, 否则 score = ln(1.3^x-y)
    当 1.3^x-y<=0 或 x<=y时, score=-1
输出:一个降序（歌曲，评分）的推荐列表
'''


def recomm_algorithm1(user_record,tag_liked_obj,tag_disliked_obj,singer_disliked_obj,singer_liked_obj,song_disliked_obj,N):
    x = 0
    y = 0
    # 所有的歌曲
    music_obj = Music.objects.all()
    # 用户听过的歌曲id列表,形如 [(3,)(4,)(9,)(3,)...]
    music_familiar = user_record.values_list('music')
    # music_familiar的数据类型不适合遍历，将它改成诸如[3,4,9,3...]的列表
    music_familiar_list = []
    for m in music_familiar:
        music_familiar_list.append(m[0])
    # list保存歌曲对象及其评分的元组，即 (music_obj,score)
    list = []
    # 遍历所有歌曲
    for m in music_obj:
        # 若歌曲的id不在用户听过的歌曲id列表中则进行评分
        if m.id not in music_familiar_list:
            # 求歌曲的标签与喜欢的标签的交集的元素个数
            x = m.tag.intersection(tag_liked_obj).count()
            # 求歌曲的标签与不喜欢的标签的交集的元素个数
            y = m.tag.intersection(tag_disliked_obj).count()
            # 若该歌曲的标签中，用户不喜欢的标签数大于等于喜欢的，或是评分函数无意义，
            # 或是不喜欢的歌手的歌,或是用户已经加入黑名单（不喜欢）的歌。则score置为-1。
            if y >= x or 1.3 ** x - y <= 0 or (m.singer in singer_disliked_obj) or (m in song_disliked_obj):
                score = -1
            elif m.singer in singer_liked_obj:
                score = math.log(1.3 ** x - y) * 1.4
            else:
                score = math.log(1.3 ** x - y)
            list.append((m.id,score))
    # 取评分前30
    sorted_list = sorted(list, key=lambda ms: ms[1], reverse=True)[:N]
    recomm_list = []
    for music_id,score in sorted_list:
        recomm_list.append(music_obj.get(id=music_id))
    return recomm_list




# 生成用户最喜爱的歌手、歌曲、歌曲风格词云
def wordcloud(id):
    user_record = Record.objects.all().filter(id=id)
    user1=user_record.values_list('user')
    # user的类型类似于(15,)，所以 user[0]才是当前用户的id，因此下面将词云保存为文件用的就是user[0]而不是user
    user = user1[0]
    music_list = ''#音乐
    singer_list = ''#歌手
    tag_list = ''#标签
    user_record = Record.objects.filter(user=user[0])#获取当前用户记录
    for u in user_record:
         music_list = music_list + u.music.name
         music_list = music_list + ' '
         singer_list = singer_list + u.music.singer.name
         singer_list = singer_list + ' '
         i = u.music.tag
         for t in u.music.tag.all():#tag是多对多，所以多重循环遍历
                tag_list = tag_list + t.tag
                tag_list = tag_list + ' '
    # 歌曲词云
    wc1=WordCloud(font_path='./fonts/simhei.ttf',
                  background_color='White',
                  collocations=False,
                  width=500, height=400).generate(music_list)
    wc1.to_file('./media/wordcloud/music_wordcloud_'+str(user[0])+'.png')#python不能自动转换
    # 歌手词云
    wc2 = WordCloud(font_path='./fonts/simhei.ttf',
                    background_color='White',
                    collocations=False,
                    width=500, height=400).generate(singer_list)
    wc2.to_file('./media/wordcloud/singer_wordcloud_'+str(user[0])+'.png')
    # 标签词云
    wc3 = WordCloud(font_path='./fonts/simhei.ttf',
                    background_color='White',
                    collocations=False, width=500, height=400).generate(tag_list)
    wc3.to_file('./media/wordcloud/tag_wordcloud_'+str(user[0])+'.png')


@login_required(login_url='/userprofile/login/')
def music_taste(request,id):
    user_record = Record.objects.filter(user=id)
    if user_record.count() >=50 :
        wordcloud(id)
        # 词云图片的 URL
        img_urls = ['/media/wordcloud/music_wordcloud_' + str(id) + '.png',
                    '/media/wordcloud/singer_wordcloud_' + str(id) + '.png',
                    '/media/wordcloud/tag_wordcloud_' + str(id) + '.png']
        context = {'img_urls': img_urls}
    # 否则不生成词云
    else:
        context = {'error':'您的播放记录过少，暂不能生成您的音乐品味！'}
    return render(request, 'music/music-taste.html', context)