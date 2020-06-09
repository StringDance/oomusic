from datetime import timezone

from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

import music


# 歌手标签：男，女，组合，内地，港台，欧美，日本，韩国，其他
# 歌手的标签主要用于歌手分类展示
class SingerTag(models.Model):
    tag = models.CharField(max_length=4)

    def __str__(self):
        return self.tag


# 创建一个标签模型而不是使用 django-taggit。
# 因为在后台给歌曲加标签时，用 taggit会增加操作难度（手打标签，用模型只需勾选项）。
# 且在用户选择喜欢和不喜欢的标签时更好处理（无论是用户角度还是后端角度）
# 歌曲标签：网络歌曲，经典老歌，情歌，儿歌，影视，乐器，DJ；伤感，快乐，安静，励志，治愈，思念，甜蜜，
# 流行，电子，轻音乐，民谣，说唱，摇滚，爵士，R&B，古典，古风，中国风，乡村，金属
# 英语，粤语，韩语，日语，国语，小语种
# 歌曲标签按类别分有很多，这里从情感、语种等四个类别选了一些标签。当然，如果觉得多，可以删，不过这没必要，放在数据库又不占地方。
class MusicTag(models.Model):
    tag = models.CharField(max_length=8)

    def __str__(self):
        return self.tag


class Singer(models.Model):
    # 歌手名，性别，标签，简介，头像
    name = models.CharField(max_length=20) # 歌手名中间不要有空格，因为歌手词云是按空格分的。详见music/views wordcloud.py：for u in user_record附近
    # 性别字段实际存储的是整数，但可通过 singer.get_gender_display可获取由 choice定义的整数到字符的映射规则。
    choices = ((1, '女'), (2, '男'), (3, '组合'))
    gender = models.IntegerField(choices=choices, default=1)
    tag = models.ManyToManyField(
        SingerTag,
        related_name='singer_tags',
        blank=True
    )
    bio = models.TextField(max_length=2000,default="这是歌手简介")
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True,default='avatar/default.jpg')

    def __str__(self):
        return self.name

    def get_gender(self):
        if self.gender:
            return "男"
        elif not self.gender :
            return "女"
        else:return "组合"


class Album(models.Model):
    # 专辑名，歌手名，封面，唱片公司，简介，发行日期
    name = models.CharField(max_length=30,null=False,default="未知专辑")
    singer = models.ForeignKey(
        Singer,
        on_delete=models.CASCADE,
    )
    album_cover = models.ImageField(
        upload_to='album-cover/%Y%m%d/',
        null=True,
        blank=True,
        default='album-cover/default_cover.jpg')
    record_company = models.CharField(max_length=20,null=True,blank=True)
    profile = models.TextField(max_length=2000,default="这是专辑简介")
    release_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    # 歌名，歌手，专辑，发行日期，作词人，作曲人，价格，播放量，标签
    name = models.CharField(max_length=50)
    # 实际上，一首歌曲可以由多位歌手演唱，这里为了简便，歌曲的演唱者只有一位。
    singer = models.ForeignKey(
        Singer,
        on_delete=models.CASCADE,  # 歌手被删除，歌曲也会被删除
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,  # 专辑删除，歌曲也会被删除
        default=1)  # ID=1是未知专辑
    release_date = models.DateField(null=True,blank=True)  # 默认认为发行日期和专辑发行日期一致，专辑日期为空，则此处的日期也为空。但是设置default=album.release_date报错。待解决
    lyricist = models.CharField(max_length=20,null=True,blank=True)
    composer = models.CharField(max_length=20,null=True,blank=True)
    price = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    total_views = models.PositiveIntegerField(default=0)
    # 注意，多对多字段的 null值不能设为True
    tag = models.ManyToManyField(
        MusicTag,
        related_name='music_tags',
        blank=True
    )

    class Meta:
        # '-release_date' 表明数据应该以发行时间倒序排列,这里暂时用字典序代替时间排序（主页上仍显示按时间排序，实际上是按字典序）
        ordering = ('-name',)

    def __str__(self):
        return self.name + ' - ' + self.singer.name

    def get_absolute_url(self):
        return reverse('music:music_detail', args=[self.id])


# 所有用户的播放记录
class Record(models.Model):
    # 用户，歌曲，播放时间
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    music = models.ForeignKey(
        Music,
        on_delete=models.CASCADE
    )

    time = models.DateTimeField(auto_now=True)  # 更新时自动写入当前时间

    class Meta:
        ordering = ('-time','user')  # 'ordering' must be a tuple or list

    def __str__(self):
        return '【' + self.user.username + '】 played 【' + self.music.name + '】at 【' + str(self.time) + '】'

    # 用户对某歌曲总的播放次数，已实现
    def music_views(self):
        # 获取当前用户的播放记录
        user_record = Record.objects.filter(user=self.user,music=self.music)
        result = user_record.count()
        return result

    # 返回用户的歌曲-播放记录字典，用于推荐
    def play_records(self):
        pass

    # 用户播放歌曲（听歌）次数,已实现
    @property
    def total_views(self):
        # 获取当前用户的播放记录
        user_record = Record.objects.filter(user=self.user)
        if user_record is None:
            return 0
        result = user_record.count()
        return result

    # 用户听过的歌曲总数(去掉重复歌曲)，有bug待解决
    @property
    def music_played(self):
        # 获取当前用户的播放记录
        user_record = Record.objects.filter(user=self.user)
        # 去重
        result = user_record.distinct(music).count()
        return result


# 歌单
class List(models.Model):
    # 用户，歌单名，标签,封面,歌单描述，播放人次,歌曲,创建时间
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30, default="新建歌单")
    tag = models.ManyToManyField(
        MusicTag,
        related_name='list_tags'
    )
    cover = models.ImageField(
        upload_to='list-cover/%Y%m%d/',
        null=True,
        blank=True,
        default='list-cover/default.jpg')
    description = models.TextField(
        max_length=600,
        null=True,
        blank=True
    )
    total_views = models.IntegerField(default=0)
    songs = models.ManyToManyField(Music)  # 歌单里的 songs 和 music 是多对多的关系
    created = models.DateTimeField(default=timezone.now)  # 创建数据时将默认写入当前的时间

    def __str__(self):
        return self.user.username + '的歌单：' + self.name

    # 获取歌单歌曲总数
    def getMusicNum(self):
        return self.songs.count()


# 每日系统推荐
class DailyRecommendation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    songs = models.ManyToManyField(Music)
    # 一个用户一天只能有一个系统推荐
    created = models.DateField(
        unique_for_date=True,
    )
