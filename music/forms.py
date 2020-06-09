from django import forms
from .models import List


# 歌单的表格类
class ListFrom(forms.ModelForm):
    class Meta:
        model = List
        fields = ('name','tag','cover','description','songs')