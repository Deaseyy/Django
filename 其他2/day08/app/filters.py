
import django_filters

from app.models import Article


class ArticleFilter(django_filters.rest_framework.FilterSet):
    # 模糊查询title字段
    title = django_filters.CharFilter(lookup_expr='contains')
    desc = django_filters.CharFilter(lookup_expr='contains')
    # id_min和id_max为接口中定义的过滤参数，其对应到数据库中查询时，对应id字段
    id_min = django_filters.CharFilter('id', lookup_expr='gte')
    id_max = django_filters.CharFilter('id', lookup_expr='lt')
    # method中定义过滤方法
    is_show = django_filters.CharFilter(method='filter_is_show')

    class Meta:
        model = Article
        # 老版本中fields中定义的参数，才是最终接口中能过滤的参数
        fields = ['title', 'desc', 'id']

    def filter_is_show(self, queryset, name, value):
        if value == 'on':
            return queryset.filter(is_show=1)
        else:
            return queryset.filter(is_show=0)
