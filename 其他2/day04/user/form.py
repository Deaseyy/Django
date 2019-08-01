
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth


class RegisterForm(forms.Form):
    # 使用表单做校验
    # 表示username字段必填，且最大不超过6字符，最小不低于3字符
    username = forms.CharField(required=True, max_length=6, min_length=3,
                               error_messages={
                                   'required': '注册用户名必填',
                                   'max_length': '注册账号最长不超过6字符',
                                   'min_length': '注册账号最小不少于3字符'
                               })
    # 表示pwd1字段必填，且最大不超过10字符，最小不低于3字符
    pwd1 = forms.CharField(required=True, max_length=10, min_length=3,
                           error_messages={
                               'required': '注册用户名必填',
                               'max_length': '注册账号最长不超过10字符',
                               'min_length': '注册账号最小不少于3字符'
                           }
                           )
    # 表示pwd2字段必填，且最大不超过10字符，最小不低于3字符
    pwd2 = forms.CharField(required=True, max_length=10, min_length=3,
                           error_messages={
                               'required': '注册用户名必填',
                               'max_length': '注册账号最长不超过10字符',
                               'min_length': '注册账号最小不少于3字符'
                           }
                           )

    def clean(self):
        # 用户名是否注册
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': '注册账号已存在，请修改账号'})
        # 校验密码是否正确
        pwd1 = self.cleaned_data.get('pwd1')
        pwd2 = self.cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError({'pwd1': '密码不一致'})
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=6, min_length=3,
                               error_messages={
                                   'required': '注册用户名必填',
                                   'max_length': '注册账号最长不超过6字符',
                                   'min_length': '注册账号最小不少于3字符'
                               })
    password = forms.CharField(required=True, max_length=10, min_length=3,
                               error_messages={
                                   'required': '注册用户名必填',
                                   'max_length': '注册账号最长不超过10字符',
                                   'min_length': '注册账号最小不少于3字符'
                               })

    def clean(self):
        # # 先校验用户对象，再校验密码
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # 校验用户名是否注册
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': '登录账号不存在，请去注册'})
        # check_password()
        # 校验密码是否正确  或者   校验密码和账号是否正确
        user = auth.authenticate(username=username,
                                 password=password)
        if not user:
            raise forms.ValidationError({'username': '账号或密码错误，请确认'})

        return self.cleaned_data

