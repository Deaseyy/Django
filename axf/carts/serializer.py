from rest_framework import serializers

from carts.models import Cart
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):

    # 使用GoodsSerializer将外键c_goods序列化,
    # 序列化后才能获取到c_goods对象的所有字段信息,否则就只是c_goods_id值
    c_goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'