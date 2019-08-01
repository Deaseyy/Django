from rest_framework import serializers

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order


class MainWheelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainWheel
        fields = ("id", "img", "name", "trackid")


class MainNavSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainNav
        fields = ("id", "img", "name", "trackid")


class MainMustBuySerializer(serializers.ModelSerializer):

    class Meta:
        model = MainMustBuy
        fields = ("id", "img", "name", "trackid")


class MainShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainShop
        fields = ("id", "img", "name", "trackid")


class MainShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainShow
        fields = "__all__"


class FoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodType
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = "__all__"


class AXFUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AXFUser
        fields = ("id", "u_username", "u_password", "u_email")


class CartSerializer(serializers.ModelSerializer):
    c_goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = ("id", "c_is_select", "c_goods_num", "c_goods")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "o_status", "o_time", "o_price")
