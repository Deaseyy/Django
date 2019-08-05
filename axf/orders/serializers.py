

from rest_framework import serializers

from goods.serializers import GoodsSerializer
from orders.models import Order, OrderGoods


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    # 重构 to_representation
    def to_representation(self, instance):  # 返回的就是instance序列化后的字典数据data
        # instance就是订单对象
        data = super().to_representation(instance)
        order_goods = instance.ordergoods_set.all()  # 对象.模型名的小写_set
        data['order_goods_info'] = OrderGoodsSerializer(order_goods,many=True).data
        return data


class OrderGoodsSerializer(serializers.ModelSerializer):
    o_goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = '__all__'