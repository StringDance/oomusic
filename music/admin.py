from django.contrib import admin

from .models import Music, Album, Singer, List, DailyRecommendation, Record, MusicTag, SingerTag

admin.site.register(Singer)
admin.site.register(Album)
admin.site.register(List)
admin.site.register(DailyRecommendation)
admin.site.register(Record)
admin.site.register(MusicTag)
admin.site.register(SingerTag)


class MusicAdmin(admin.ModelAdmin):
    # 设置fieldsets 控制管理“添加”和 “更改” 页面的布局.
    fieldsets = [
        ('Basic information',  {'fields': ('name','singer','album')}),
        ('More information', {'fields': ('lyricist','composer','price','release_date','total_views','tag')}),
    ]


admin.site.register(Music, MusicAdmin)
