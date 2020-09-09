from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.UserAuthentication import GeneralAuthentication, UserAuthentication
from api.models import User
from home.circle.models import News, Comment
from home.circle.serializers import ListNewsSerializer, CreateNewsSerializer, ListCommentSerializer, CreateCommentSerializer


class NewsView(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = ListNewsSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        # # 进入详情页时获取token，添加访问信息
        # # （前端在请求头中传递Authorization:token,后端用HTTP_AUTHORIZATION接收）
        # # todo：不过下面的功能都可以在认证组件中完成
        # token = request.META.get('HTTP_AUTHORIZATION',None)
        # if not token:
        #     return response
        # user_obj = User.objects.filter(token=token).first()
        # if not user_obj:
        #     return response

        # # 判断当前用户是否有访问此新闻的记录
        # # todo：(Viewer访问记录表需要新建，这里暂时没有设计一个访问记录表，
        # # todo:只单独在news建了一个访问次数的字段viewer_count)，下面这块功能先省略，以后再加
        # pk = kwargs.get('pk')
        # exists = Viewer.objects.filter(user_obj,news_id=pk).exists()
        # News.objects.filter(id=pk).update(viewer_count=F('viewer_count')+1)
        # if exists:
        #     return response
        return response

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to return `self.serializer_class`.
        """
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            return CreateNewsSerializer


    def perform_create(self, serializer):
        serializer.save(user_id=1)


class CommentView(APIView):

    # def get_authenticators(self):
    # # 根据不同请求方法接口，使用不同认证组件
    #     if self.request.method == 'POST':
    #         return [GeneralAuthentication(), ]
    #     return [UserAuthentication(), ]

    def get(self,request,*args, **kwargs):
        """获取这个根评论的所有子评论"""
        root_id = request.query_params.get('root')
        child_comments = Comment.objects.filter(root_id=root_id).order_by('id')
        ser = ListCommentSerializer(instance=child_comments,many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # 1 数据校验
        # 2 校验通过保存到数据库
        # 3 将保存的数据再返回给前端展示
        ser = CreateCommentSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user_id=1)  # 写死为1，应从token获取用户
            news_id = ser.data.get('news')
            News.objects.filter(id=news_id).update(comment_count=F('comment_count')+1)
            return Response(data=ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)