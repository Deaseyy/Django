import django_filters

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    # typeid  childid  order_rule
    typeid = django_filters.CharFilter('categoryid') # id为精确查询,无需lookup参数,typeid对应数据库categoryid参数
    childcid = django_filters.CharFilter(method='filter_child')  # 当过滤字段与数据字段一样时括号内可不定义
    order_rule = django_filters.CharFilter(method='filter_rule')

    class Meta:
        model = Goods
        fields = ['categoryid']

    # 子分类过滤
    def filter_child(self,queryset, name, value):
        if value == '0':  # 若child_value=0,则child_name为全部分类
            return queryset
        else:             # child_value为其他值:根据值来过滤
            return queryset.filter(childcid=value)


    # 排序过滤
    def filter_rule(self,queryset, name, value):
        if value == '0':    # 'order_name': '综合排序', 'order_value':0
            return queryset
        elif value == '1':  # 'order_name': '价格升序', 'order_value':1
            return queryset.order_by('price')
        elif value == '2':  # 'order_name': '价格降序', 'order_value':2
            return queryset.order_by('-price')
        elif value == '3':  # 'order_name': '销量升序', 'order_value':3
            return queryset.order_by('productnum')
        else:               # 'order_name': '销量降序', 'order_value':4
            return queryset.order_by('-productnum')