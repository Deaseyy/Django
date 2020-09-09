import random

from rest_framework.decorators import api_view

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models, logic
from api.models import Photos
from api.serializers import LoginSerializer, SmsCodeSerializer, PhotosSerializer


class LoginView(APIView):
    def post(self,request):
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 500, 'msg':'登陆失败！'})
        phone = ser.validated_data.get('phone')
        avatar = ser.validated_data.get('avatar')
        nick = ser.validated_data.get('nick')
        user_obj,flag = models.User.objects.get_or_create(phone=phone)
        print(user_obj, flag)
        token = logic.get_token(user_obj)
        print(token)
        # 获取当前微信用户的信息，保存到数据库
        user_obj.avatar = avatar
        user_obj.nick = nick
        user_obj.save()
        return Response({'token': token, 'code':200,'msg':'登陆成功！'})


class SmsCodeView(APIView):
    def get(self,request):
        """
        1.获取手机号
        2.手机格式校验
        3.生成随机验证码
        4.保存手机号+验证码（40s过期）
        """
        ser = SmsCodeSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'code':500,'msg':'手机格式错误！'})
        phone = ser.validated_data.get('phone')
        sms_code = random.randint(1000, 9999)
        print(sms_code)
        conn = get_redis_connection()
        conn.set(phone,sms_code,ex=40)
        return Response({'code': 200, 'sms_code': sms_code})


class PhotosView(APIView):
    def get(self, request):
        queryset = Photos.objects.all()
        ser = PhotosSerializer(queryset, many=True)
        return Response({'code':200, 'data':ser.data})

    def post(self, request):
        img_url = request.data.get('img_url')
        print(img_url)
        if not img_url:
            return Response({'code': 500, 'msg': '请先选择图片再上传！'})
        img_url = f'https://{img_url}'
        Photos.objects.create(img_url=img_url)
        return Response({'code': 200, 'msg': '图片上传成功！'})











