from django.contrib import admin

from goods.models import FoodType, Goods

# 将模型AXFUser交给后台进行管理
admin.site.register(FoodType)
admin.site.register(Goods)
