# 引入表单类
#Form表单的功能
#自动生成HTML表单元素
#检查表单数据的合法性
#如果验证错误，重新显示表单（数据不会重置）
#数据类型转换（字符类型的数据转换成相应的Python类型）
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile, LikesAndDislikes


# 登录表单，继承了 forms.Form 类
# forms.Form需要手动配置每个字段，它适用于不与数据库进行直接交互的功能。
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')


# 用户偏好表单
class LikesAndDislikesForm(forms.ModelForm):
    class Meta:
        model = LikesAndDislikes
        fields = ('singer_liked','singer_disliked','tag_liked','tag_disliked','song_disliked')
