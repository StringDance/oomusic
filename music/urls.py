from .import views
from django.urls import path

app_name = 'music'

urlpatterns = [
    # 歌曲列表（主页）
    path('', views.index, name='index'),
    # 歌曲列表（主页）
    path('list/', views.music_list, name='music_list'),
    # 歌曲详情
    path('detail/<int:id>/', views.music_detail, name='music_detail'),
    # 专辑详情
    path('album-detail/<int:album_id>/', views.album_detail, name='album_detail'),
    # 首页播放歌曲
    path('play/<int:id>/', views.music_play, name='music_play'),
    # 推荐页播放歌曲
    path('play2/<int:id>/', views.music_play2, name='music_play2'),
    # 详情页播放歌曲
    path('play3/<int:id>/', views.music_play3, name='music_play3'),
    # 歌手详情
    path('singer-detail/<int:singer_id>/', views.singer_detail, name='singer_detail'),
    # 播放记录
    path('record-detail/<int:user_id>',views.record_detail,name='record_detail'),
    # 今日推荐
    path('daily-recommendation/<int:id>',views.daily_recommendation,name='daily_recommendation'),
    # 删除评论
    path('comment-delete/<int:comment_id>',views.comment_delete,name='comment_delete'),
    # 喜欢歌手
    path('follow/<int:id>/',views.follow,name='follow'),
    # 拉黑（不喜欢）歌手
    path('blacklist/<int:id>/',views.blacklist,name='blacklist'),
    # 屏蔽歌曲
    path('shield/<int:id>/',views.shield,name='shield'),
    # 听歌品味
    path('music-taste/<int:id>/',views.music_taste,name='music_taste')
]