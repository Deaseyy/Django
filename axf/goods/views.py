import json

from django.shortcuts import render


# def home():
#     return JsonResponse()
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework.views import APIView

from goods.filters import GoodsFilter
from goods.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods
from goods.serializers import MainWheelSerializer, MainNavSerializer, MainMustBuySerializer, MainShopSerializer, \
    MainShowSerializer, FoodTypeSerializer, GoodsSerializer


# class方法,官网提供
class Home(APIView):
    def get(self):
        pass
# 函数方法,写if条件区分请求方法
@api_view(['GET'])   # 使用模型过多,不是确定的资源,不能直接使用继承mixins的方式,需自己定义
def home(request):
    # if request.method=='GET':  # 这样写

    # 优化,使用redis进行缓存,降低数据库的访问压力
    # 有序集合,无序集合,字符串,hash,列表
    # hash: key field value
    # hash: goods  mainwheels MainWheelSerializer(main_wheels, many=True).data,
    #       goods  main_navs  'main_navs': MainNavSerializer(main_navs, many=True).data,

    # 使用原生redis, redis.Redis(host,port,..)
    conn = get_redis_connection()

    if not conn.hget('goods','main_wheels'):  # 若从redis获取不到
        mainwheels = MainWheel.objects.all()   # 从mysql数据库取出数据
        value = MainWheelSerializer(mainwheels, many=True).data  #序列化
        value = json.dumps(value)
        conn.hset('goods', 'main_wheels', value)   # 存入redis
    redis_main_wheels = json.loads(conn.hget('goods', 'main_wheels'))

    if not conn.hget('goods', 'main_navs'):  # 若从redis获取不到
        mainnavs = MainNav.objects.all()  # 从mysql数据库获取对象
        value = MainNavSerializer(mainnavs, many=True).data  #将对象序列化
        # 将序列化后的字典形式转换为json格式数据,再存入
        value = json.dumps(value)
        conn.hset('goods', 'main_navs', value)    # 存入redis
        # 取出时,将json格式数据转为字典形式
    redis_main_navs = json.loads(conn.hget('goods', 'main_navs'))   # 从redis取出数据

    if not conn.hget('goods', 'main_mustbuys'):  # 若从redis获取不到
        mainmustbuys = MainMustBuy.objects.all()  # 从mysql数据库获取
        value = MainMustBuySerializer(mainmustbuys, many=True).data
        value = json.dumps(value)
        conn.hset('goods', 'main_mustbuys', value)
    redis_main_mustbuys = json.loads(conn.hget('goods', 'main_mustbuys'))

    if not conn.hget('goods', 'main_shops'):  # 若从redis获取不到
        mainshops = MainShop.objects.all()  # 从mysql数据库获取
        value = MainShopSerializer(mainshops, many=True).data
        value = json.dumps(value)
        conn.hset('goods', 'main_shops', value)
    redis_main_shops = json.loads(conn.hget('goods', 'main_shops'))

    if not conn.hget('goods', 'main_shows'):  # 若从redis获取不到
        mainshows = MainShow.objects.all()  # 从mysql数据库获取
        value = MainShowSerializer(mainshows, many=True).data
        value = json.dumps(value)
        conn.hset('goods', 'main_shows', value)
    redis_main_shows = json.loads(conn.hget('goods', 'main_shows'))

    res = {
        'main_wheels': MainWheelSerializer(redis_main_wheels, many=True).data,
        'main_navs': MainNavSerializer(redis_main_navs, many=True).data,
        'main_mustbuys': MainMustBuySerializer(redis_main_mustbuys, many=True).data,
        'main_shops': MainShopSerializer(redis_main_shops, many=True).data,
        'main_shows': MainShowSerializer(redis_main_shows, many=True).data,
    }
    return Response(res)
    # 直接从mysql数据库取数据,多用户访问时,数据库的访问压力太大
    # main_wheels = MainWheel.objects.all()
    # main_navs = MainNav.objects.all()
    # main_mustbuys = MainMustBuy.objects.all()
    # main_shops = MainShop.objects.all()
    # main_shows = MainShow.objects.all()
    # res = {
    #     'main_wheels': MainWheelSerializer(main_wheels, many=True).data,
    #     'main_navs': MainNavSerializer(main_navs, many=True).data,
    #     'main_mustbuys': MainMustBuySerializer(main_mustbuys, many=True).data,
    #     'main_shops': MainShopSerializer(main_shops, many=True).data,
    #     'main_shows': MainShowSerializer(main_shows, many=True).data,
    # }
    # return Response(res)


class FoodTypeView(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    queryset =FoodType.objects.all()
    serializer_class = FoodTypeSerializer

    # FoodType模型中,前端只需要foodtypes数据,
    # 所以请求/api/goods/foodtype/,直接使用ListModelMixin源码中的list方法就能返回分类,无需重构.
    # 获取分类响应结果:{code:200,msg:'',data:{全部的foodtype信息}}


class MarketView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):

    queryset = Goods.objects.all()   # 必给参数
    serializer_class = GoodsSerializer  # 必给参数
    filter_class = GoodsFilter      # 过滤参数配置

    def list(self, request, *args, **kwargs):
        # 查询商品信息
        # filter_queryset()调用filter_class,过滤问号后传的参数条件
        # 根据前端请求参数过滤 /api/goods/market.md/?typeid=104749&childcid=0&order_rule=0
        queryset = self.filter_queryset(self.get_queryset())  # filter_queryset() 会自动调用filter_class=GoodsFilter类去过滤
        serializer = self.get_serializer(queryset,many=True)

        typeid = self.request.query_params.get('typeid')
        food_type = FoodType.objects.filter(typeid=typeid).first()
        # 全部分类:0#进口水果:103534#国产水果:103533
        # 方式一: for循环取子类分类信息
        # foodtype_childname_list = []
        # for childnames in food_type.childtypenames.split('#'):
        #     data = {
        #         'child_name': childnames.split(':')[0],
        #         'child_value': childnames.split(':')[1],
        #     }
        #     foodtype_childname_list.append(data)

        # 方式二:列表生成式
        foodtype_childname_list=[{'child_name':childnames.split(':')[0], 'child_value':childnames.split(':')[1]} for childnames in food_type.childtypenames.split('#')]

        # 排序  自己定义值
        order_rule_list = [
            {'order_name': '综合排序', 'order_value':0},
            {'order_name': '价格升序', 'order_value':1},
            {'order_name': '价格降序', 'order_value':2},
            {'order_name': '销量升序', 'order_value':3},
            {'order_name': '销量降序', 'order_value':4},
        ]

        # 根据前端所需要的数据,来重构响应结果
        res = {
            'goods_list': serializer.data,
            'order_rule_list': order_rule_list,
            'foodtype_childname_list': foodtype_childname_list,
        }
        return Response(res)