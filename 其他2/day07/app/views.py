from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from app.models import Article
from app.serializers import ArticleSerializer


def index(request):
    if request.method == 'GET':
        return HttpResponse('index')


def add_art(request):
    if request.method == 'GET':
        return render(request, 'article.html')

    if request.method == 'POST':

        pass


class ArticleView(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    # 资源对应的所有数据
    queryset = Article.objects.all()
    # 序列化
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        # get_queryset()获取上面定义的queryset值
        queryset = self.get_queryset()
        # get_serializer()调用上面定义的ArticleSerializer
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_show = 0
        instance.save()