
from rest_framework import serializers

from goods.models import Goods, MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType
from orders.models import OrderGoods


class MainWheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainWheel
        fields = '__all__'



class MainNavSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainNav
        fields = '__all__'

class MainMustBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMustBuy
        fields = '__all__'

class MainShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainShop
        fields = '__all__'


class MainShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainShow
        fields = '__all__'


class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields = '__all__'



class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'

