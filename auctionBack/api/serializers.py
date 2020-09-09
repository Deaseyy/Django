import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Photos, User


def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$",value):
        raise ValidationError('手机格式错误')
    return value


class SmsCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[phone_validator])


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[phone_validator])
    sms_code = serializers.CharField(max_length=4)
    avatar = serializers.CharField(max_length=500)
    nick = serializers.CharField(max_length=255)

    def validate_code(self, value):
        if len(value) != 4 or not value.isdecimal():
            raise ValidationError('短信格式错误')
        # is_valid之前取值用initial_data
        phone = self.initial_data.get('phone')
        conn = get_redis_connection()
        code = conn.get(phone)
        if value != code.decode('utf-8'):
            raise ValidationError('短信验证码错误')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PhotosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photos
        fields = "__all__"





