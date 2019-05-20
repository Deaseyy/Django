from django.db import models

# Create your models here.


# ORDER_STATUS
# 已下单未付款
from goods.models import Goods
from user.models import AXFUser

ORDER_STATUS_NOT_PAY = 0
# 已下单已付款未发货
ORDER_STATUS_NOT_SEND = 2
# 已下单已付款已发货未收货
ORDER_STATUS_NOT_RECEIVE = 3
# 已下单已付款已发货已收货未确认
# 已下单已付款已发货已收货已确认未评价
# 已下单已付款已发货已收货已确认已评价未追评
# 已下单已付款已发货已收货已确认已评价
    # 申请售后
        # 退货
        # 换货
        # 返修

class Order(models.Model):
    o_user = models.ForeignKey(AXFUser, on_delete=models.CASCADE)
    o_price = models.FloatField(default=0,)
    o_time = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=ORDER_STATUS_NOT_PAY)

    class Meta:
        db_table = 'axf_order'


class OrderGoods(models.Model):  # 订单中商品详情表
    o_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    o_goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    o_goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_ordergoods'