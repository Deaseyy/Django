from django import forms

from user.models import User


class registerForm(forms.Form):
    '验证字段名要和html表单的input框name字段一致,才能验证'
    user_name = forms.CharField(max_length=20, min_length=2,required=True,
                               error_messages={'required': '用户名为必填',
                                               'max_length': '最大长度为20个字符',
                                               'min_length': '最小长度为3个字符'})
    pwd = forms.CharField(max_length=255, min_length=3,required=True,
                               error_messages={'required': '密码为必填',
                                               'max_length': '最大长度为20个字符',
                                               'min_length': '最小长度为3个字符'})
    cpwd = forms.CharField(max_length=255, min_length=3, required=True,
                               error_messages={'required': '密码为必填',
                                               'max_length': '最大长度为20个字符',
                                               'min_length': '最小长度为3个字符'})
    # email = forms.RegexField('^\d+@qq\.com&', max_length=100, required=True,
    #                          error_messages={'require': '邮箱为必填',
    #                                          'regex': '邮箱格式不正确'})
    email = forms.CharField(max_length=100, required=True, error_messages={'require': '邮箱为必填'})


    def clean(self):  # 未定义时调用默认clean方法
        # 用户名是否注册
        username = self.cleaned_data.get('user_name')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'user_name': '该用户名已被注册!'})

        # 校验密码是否正确
        pwd1 = self.cleaned_data.get('pwd')
        pwd2 = self.cleaned_data.get('cpwd')
        if pwd1 != pwd2:
            raise forms.ValidationError({'pwd':'重复密码不一致!'})
        return self.cleaned_data


class loginForm(forms.Form):
    '验证字段名要和html表单的input框name字段一致,才能验证'
    username = forms.CharField(max_length=20, min_length=2,required=True,
                               error_messages={'required': '请输入用户名!',
                                               'max_length': '最大长度为20个字符!',
                                               'min_length': '最小长度为3个字符!'})
    password = forms.CharField(max_length=255, min_length=3,required=True,
                               error_messages={'required': '请输入密码!'})

    # 只校验username字段
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户不存在!')
        return username


class addressForm(forms.Form):
    name = forms.CharField(max_length=20,min_length=2,required=True,
                           error_messages={
                               'required': '请输入收件人姓名!',
                               'max_length': '最大长度为20字符!',
                               'min_length': '最小长度为2字符!',
                           })
    site = forms.CharField(max_length=100,min_length=5,required=True,
                           error_messages={
                               'required': '请输入收件人地址!',
                               'max_length': '最大长度为100字符!',
                               'min_length': '最小长度为5字符!',
                           })
    postcode = forms.CharField(max_length=10,min_length=5,required=True,
                           error_messages={
                               'required': '请输入收件人所在地邮编!',
                               'max_length': '最大长度为10字符',
                               'min_length': '最小长度为5字符',
                           })
    tel = forms.CharField(max_length=11,min_length=4,required=True,
                           error_messages={
                               'required': '请输入收件人电话!',
                               'max_length': '手机号码最长11字符!',
                               'min_length': '手机号码最短4字符!',
                           })