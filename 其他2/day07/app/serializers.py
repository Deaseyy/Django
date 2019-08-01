
from rest_framework import serializers

from app.models import Article


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
        fields = ['title', 'desc', 'id']
