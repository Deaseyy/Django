
from rest_framework import serializers
from rest_framework.response import Response

from app.models import Article
from utils.errors import ParamsException


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=10, min_length=5,
                                  error_messages={
                                      'required': '标题必填',
                                      'max_length': '标题不能超过10字符',
                                      'min_length': '标题不能短于5字符'
                                  })
    desc = serializers.CharField(required=False)

    class Meta:
        # 序列化的模型定义
        model = Article
        fields = ['title', 'desc', 'id', 'is_show']

    def validate(self, attrs):
        # 校验文章标题是否重复
        title = attrs.get('title')
        if title:
            if Article.objects.filter(title=title).exists():
                raise ParamsException({'code': 1002, 'msg': '标题重复'})
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_show'] = '展示' if data['is_show'] else '不展示'
        return data
