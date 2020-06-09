from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from wordcloud import WordCloud

from music.models import Music, Singer, Record
from .models import MusicTag, LikesAndDislikes
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from .forms import UserLoginForm, UserRegisterForm, ProfileForm, LikesAndDislikesForm

# Create your views here.
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("music:index")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("music:index")


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            # 保存好数据后立即登录并跳转到主页
            return redirect('music:index')
        else:
            return HttpResponse("填写错误")
    elif request.method == 'GET':
        HttpResponse("SSS")
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# @login_required要求调用user_delete()函数时，用户必须登录；
# 如果未登录则不执行函数，将页面重定向到/userprofile/login/地址去。
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            #退出登录，删除数据并返回主页
            logout(request)
            user.delete()
            return redirect("music:index")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    user_record = Record.objects.filter(user=user)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
        #上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("表单输入有误。请重新输入~")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户填写偏好
@login_required(login_url='/userprofile/login/')
def user_preference(request,id):
    tags = MusicTag.objects.all()
    music = Music.objects.all()
    singers = Singer.objects.all()
    user = User.objects.get(id=id)
    # 获取偏好信息，若不存在则创建
    # 注意 user__id是双下划线。
    # 若用user__id=id则新用户填写时会报错 NOT NULL constraint failed: userprofile_likesanddislikes.user_id
    likes_dislikes = LikesAndDislikes.objects.get_or_create(user=user)[0]
    # 验证登录用户、请求填写偏好用户是否相同
    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
        form = LikesAndDislikesForm(request.POST)
        if form.is_valid():
            # 取得清洗后的合法数据（数据会被自动转换为Python对象）
            data_cd = form.cleaned_data
            # 将数据赋值给字段，因为这几个字段全都是多对多类型，所以注意后面要接_set，否则报错：
            # Direct assignment to the forward side of a many-to-many set is prohibited.
            # Use singer_liked.set() instead.
            #data_cd['singer_liked']是 QuerySet类型
            likes_dislikes.singer_liked.set(data_cd['singer_liked'])
            likes_dislikes.singer_disliked.set (data_cd['singer_disliked'])
            likes_dislikes.tag_disliked.set (data_cd['tag_disliked'])
            likes_dislikes.tag_liked.set (data_cd['tag_liked'])
            likes_dislikes.song_disliked.set ( data_cd['song_disliked'])
            likes_dislikes.save()
            return redirect("userprofile:preference",id = id)
        else:
            return HttpResponse("表单输入有误。请重新输入~")
    elif request.method == 'GET':
        form = LikesAndDislikesForm()
        context = {'form': form, 'likes_dislikes': likes_dislikes,
                   'user': user, 'tags':tags,'singers':singers,'music':music
        }
        return render(request, 'userprofile/preference.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
