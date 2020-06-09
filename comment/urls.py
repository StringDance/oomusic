from .import views
from django.urls import path

app_name = 'comment'

urlpatterns = [
    # 处理一级回复
    path('post-comment/<int:music_id>/', views.post_comment, name='post_comment'),
    # 处理二级回复
    path('post-comment/<int:music_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]