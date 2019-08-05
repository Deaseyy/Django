import re
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from rest_framework import serializers

from user.models import AXFUser
from utils.errors import ParamsException


class UserSerializer(serializers.ModelSerializer):
    # 继承ModelSerializer,可序列化,可校验字段,无需自定义字段
    class Meta:
        model = AXFUser
        fields = '__all__'


class UserRegisterSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=10,min_length=3,
                                       error_messages={
                                           'required': '注册账号必填!',
                                           'blank': '注册账号不能为空',  # 该参数需填写,否则返回英文
                                           'max_length': '账号最长10字符',
                                           'min_length': '账号最短3字符',
                                       })
    u_password = serializers.CharField(required=True, max_length=10,min_length=5,
                                       error_messages={
                                           'required': '注册密码必填!',
                                           'blank': '注册密码不能为空',
                                           'max_length': '密码最长10字符',
                                           'min_length': '密码最短5字符',
                                       })
    u_password2 = serializers.CharField(required=True, max_length=10,min_length=5,
                                       error_messages={
                                           'required': '确认密码必填!',
                                           'blank': '确认密码不能为空',
                                           'max_length': '确认密码最长10字符',
                                           'min_length': '确认密码最短5字符',
                                       })
    u_email = serializers.CharField(required=True,
                                       error_messages={
                                           'required': '邮箱必填!',
                                           'blank': '注册邮箱不能为空',
                                       })

    def validate(self, attrs):  #上面字段校验通过后,才会执行该方法
        # 1.注册账号是否存在
        # 2.注册密码和确认密码是否一致
        # 3.邮箱正则是否匹配
        # 如果以上校验有问题,则抛异常
        username = attrs.get('u_username')
        password = attrs.get('u_password')
        password2 = attrs.get('u_password2')
        email = attrs.get('u_email')
        # if username:  # 无需判断是否为空,上面已经校验
        if AXFUser.objects.filter(u_username=username).exists():
            raise ParamsException({'code':1001, 'msg':'用户名已存在!'})
        if password != password2:
            raise ParamsException({'code': 1002, 'msg': '确认密码不一致!'})
        if not re.match('.+@qq.com$', email):
            raise ParamsException({'code': 1003, 'msg': '邮箱格式不对!'})
        return attrs


    def register_user(self,validate_attr):
        # 注册
        username = validate_attr.get('u_username')
        password = make_password(validate_attr.get('u_password'))
        email = validate_attr.get('u_email')
        user = AXFUser.objects.create(u_username=username,
                               u_password=password,
                               u_email=email)
        return user


class UserLoginSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=10, min_length=3,
                                       error_messages={
                                           'required': '账号必填!',
                                           'blank': '账号不能为空',  # 该参数需填写,否则返回英文
                                           'max_length': '最长10字符',
                                           'min_length': '最短3字符',
                                       })
    u_password = serializers.CharField(required=True, max_length=10, min_length=5,
                                       error_messages={
                                           'required': '密码必填!',
                                           'blank': '密码不能为空',
                                           'max_length': '密码最长10字符',
                                           'min_length': '密码最短5字符',
                                       })

    def validate(self, attrs):
        # 1.判断账号是否存在
        # 2.判断密码是否正确
        username = attrs.get('u_username')
        password = attrs.get('u_password')
        user = AXFUser.objects.filter(u_username=username).first()
        if not user:
            raise ParamsException({'code': 1004,'msg':'账号不存在!'})
        if not check_password(password,user.u_password):
            raise ParamsException({'code': 1005,'msg':'密码错误!'})
        return attrs


    def login_user(self,validate_attr):
        # 登陆,设置并返回token参数给前端,且保存token参数到redis
        token = uuid.uuid4().hex
        username = validate_attr.get('u_username')
        user = AXFUser.objects.filter(u_username=username).first()
        # 后端使用redis保存
        cache.set(token, user.id, timeout=86400) # 导包注意 from django.core.cache import cache
        return token








































