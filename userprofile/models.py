# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# 用户扩展信息
from music.models import Singer, MusicTag, Music


class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    # ImageField字段不会存储图片本身，而仅仅保存图片的地址。
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True,default='avatar/default.jpg')
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


# 用户喜好和厌恶信息(偏好)，用于解决推荐系统冷启动问题和精准推荐、屏蔽。
# 下面所有内容都不强制用户填，但如果某些内容不填的话就无法在用户积累一定听歌记录之前进行每日推荐，这个后果应该告知用户。
# 用多对多关系的好处是可以双向查询.
class LikesAndDislikes(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='likes_dislikes'
    )
    # 喜欢的歌手（关注的歌手）
    singer_liked = models.ManyToManyField(
        Singer,
        related_name='singer_liked',
        blank=True
    )
    # 不喜欢的歌手（歌手黑名单）
    singer_disliked = models.ManyToManyField(
        Singer,
        related_name='singer_disliked',
        blank=True
    )
    # 喜欢的标签（喜欢的歌曲风格）
    tag_liked = models.ManyToManyField(
        MusicTag,
        related_name='tag_liked',
        blank=True
    )
    # 不喜欢的标签（不喜欢的歌曲风格）
    tag_disliked = models.ManyToManyField(
        MusicTag,
        related_name='tag_disliked',
        blank=True
    )
    # 屏蔽的歌曲(被屏蔽的歌曲不会被推荐)
    song_disliked = models.ManyToManyField(
        Music,
        related_name='song_disliked',
        blank=True
    )


