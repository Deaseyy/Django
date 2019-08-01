from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from app.filters import ArticleFilter
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
    # 过滤
    filter_class = ArticleFilter

    # def get_queryset(self):
    #     title = self.request.query_params.get('title')
    #     desc = self.request.query_params.get('desc')
    #     is_show = self.request.query_params.get('is_show')
    #     if title and not desc:
    #         return self.queryset.filter(title=title)
    #     if not title and desc:
    #         return self.queryset.filter(desc__contains=desc)
    #     if title and desc:
    #         return self.queryset.filter(title__contains=title, desc__contains=desc)
    #     if not title and not desc:
    #         return self.queryset


    # def list(self, request, *args, **kwargs):
    #     # get_queryset()获取上面定义的queryset值
    #     queryset = self.get_queryset()
    #     # get_serializer()调用上面定义的ArticleSerializer
    #     serializer = self.get_serializer(queryset, many=True)
    #     # res = {
    #     #     'code': 200,
    #     #     'msg': '请求成功',
    #     #     'data': serializer.data
    #     # }
    #     return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_show = 0
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        res = {
            'code': 200,
            'msg': '请求成功'
        }
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            res['data'] = serializer.data
        except:
            res['code'] = 1001
            res['msg'] = '请求失败，文章不存在'
        return Response(res)
