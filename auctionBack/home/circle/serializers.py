import collections

from django.db.models import Max
from django.forms import model_to_dict
from rest_framework import serializers

from api.serializers import UserSerializer
from home.circle.models import News, NewsDetail, Comment

"""
注意事项：
1. 创建时不需要的表格字段必须exclude或设置readonly，谨防前端传递直接改变（比如点赞数，浏览数）

2. 展示关联表的信息
    a.（一对一，一对多）模型中如果有外键属性需要展示，可直接使用嵌套序列化；
    b. 不带ForeignKey的一方，需要展示关联表属性时，在to_representation中序列化对象，添加到data;
    c. 还可以通过SerializerMethodField()指定方法 get_字段名 返回关联表的信息
"""

class ImageSerializer(serializers.Serializer):
    key = serializers.CharField()
    cos_url = serializers.CharField()


class CreateNewsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = News
        exclude = ['user','like_count','viewer_count','comment_count']

    def create(self, validated_data):
        images = validated_data.pop('images')  # 提出图片列表
        # 保存news表数据
        news_obj = News.objects.create(**validated_data)
        # 保存newsdetail表数据（多条）
        data_list = NewsDetail.objects.bulk_create(
            [NewsDetail(**info, news=news_obj) for info in images]
        )
        news_obj.images = data_list

        return news_obj



class ListNewsSerializer(serializers.ModelSerializer):
    """ 正常应该将列表序列化器和详情序列化器分开写，不然列表页多出许多详情页的无用字段
        这里暂时就使用一个序列化器
    """
    user = UserSerializer()  # 这里定义user后,下面的read_only_fields中只读属性将失效
    add_time = serializers.DateTimeField(format="%Y-%m-%d %X",read_only=True) # 若这里去掉只读，放在下面也不会生效
    # images = ImageSerializer(many=True)  # 模型中不带这个字段，识别不到（可以添加到fields中，要拆掉fields比较麻烦）
    # 通过SerializerMethodField获取关联表信息
    images = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # todo：这也是一种返回关联表信息的方法
    #     images = instance.newsdetail_set.all()  # 对象.模型名的小写_set.all()
    #     data['images'] = ImageSerializer(images, many=True).data
    #     return data

    def get_images(self, instance):
        # 加入只想返回外键关联字段的部分信息，也可以通过SerializerMethodField
        cos_url = [obj.cos_url for obj in instance.newsdetail_set.all()]
        return cos_url

    def get_comment(self, instance):
        """
        获取所有的1级评论，再给每个1级评论获取一个2级评论
        """
        # 1.获取所有一级评论
        first_comments = Comment.objects.filter(news=instance, depth=1
            ).order_by('-id').values(
            'id','content','depth','user__nick','user__avatar','add_time')
        first_id_list = [item['id'] for item in first_comments]
        # # 2.获取当前已取一级评论下的所有二级评论 (不是需求)
        # second_comments = Comment.objects.filter(news=instance, depth=2,reply_id__in=first_id_list)
        # 2.获取当前已取一级评论下的二级评论(只取每个1级下的最新一条二级评论)；即:根据reply_id分组，取id最大的那条
        result = Comment.objects.filter(news=instance, depth=2, reply_id__in=first_id_list
                        ).values('reply_id').annotate(max_id=Max('id'))
        second_id_list = [item['max_id'] for item in result]  # 各一级下最新2级评论id
        second_comments = Comment.objects.filter(id__in=second_id_list).values(
            'id','content','depth','user__nick','user__avatar','add_time','reply_id','reply__user__nick')

        # 构造格式，将二级评论插入到对应一级评论下
        first_dict = collections.OrderedDict()
        for item in first_comments:
            item['add_time'] = item['add_time'].strftime('%Y-%m-%d %X')
            first_dict[item['id']] = item

        for node in second_comments:
            first_dict[node['reply_id']]['child'] = [node,]

        return first_dict.values()


class ListCommentSerializer(serializers.ModelSerializer):
    """评论模型序列化器 (查看更多评论时使用)"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %X')
    # 必须和第一次取详情页评论数据时的child结构字段一致；点击获取更多才能直接覆盖child
    # user = serializers.SerializerMethodField()  # 也可直接使用嵌套序列化
    # reply_user = serializers.SerializerMethodField()
    user__nick = serializers.CharField(source='user.nick')
    user__avatar = serializers.CharField(source='user.avatar')
    reply_id = serializers.CharField(source='reply.id')
    reply__user__nick = serializers.CharField(source='reply.user.nick')


    class Meta:
        model = Comment
        exclude = ['news','user','reply','root']

    # def get_user(self,instance):
    #     return model_to_dict(instance.user, fields=['id','nick','avatar'])
    #
    # def get_reply_user(self,instance):
    #     return model_to_dict(instance.reply.user, fields=['id','nick'])


class CreateCommentSerializer(serializers.ModelSerializer):
    # 需要返回和之前评论数据一致的结构，增加几个序列化展示的字段-->设为只读,前端可不传，无需校验，返回的时候会增加这些字段
    add_time = serializers.DateTimeField(format='%Y-%m-%d %X',read_only=True)
    user__nick = serializers.CharField(source='user.nick',read_only=True)
    user__avatar = serializers.CharField(source='user.avatar',read_only=True)
    reply_id = serializers.CharField(source='reply.id',read_only=True)
    reply__user__nick = serializers.CharField(source='reply.user.nick',read_only=True)

    class Meta:
        model = Comment
        # exclude = ['user', 'favor_count']
        exclude = ['user']










