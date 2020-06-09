# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from music.models import Music
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


# 歌曲的评论
class Comment(MPTTModel):
    music = models.ForeignKey(
        Music,
        on_delete=models.CASCADE, # 歌曲被删除，评论也会被删除
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # 用户被删除，评论也会被删除
        related_name='comments'
    )
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    # mptt树形结构,用于存储数据之间的关系
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['-created']

    def __str__(self):
        return self.content[:30]