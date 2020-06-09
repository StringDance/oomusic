from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from music.models import Music
from .forms import CommentForm
from .models import Comment


# 发表评论。
# parent_comment_id为父评论的id值，同时将缺省值设为None(因为有两个path共用这个视图函数)，
# 设为none表示为一级评论,否则就是多级评论。
@login_required(login_url='/userprofile/login/')
def post_comment(request, music_id, parent_comment_id=None):
    music = get_object_or_404(Music, id=music_id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.music = music
            new_comment.user = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级。
                # get_root()方法将其父级重置为树形结构最底部的一级评论
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')
            new_comment.save()
            # redirect()返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面。
            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法。
            return redirect(music)
        else:
            return HttpResponse("内容有误，请重新填写。")
    # 处理GET请求，给二级回复提供空白的表单。
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'music_id': music_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
        # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")