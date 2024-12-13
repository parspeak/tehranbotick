import django_filters
from products.models import Product
from datetime import datetime


class ProductFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='variants__price', lookup_expr='gte', distinct=True)
    price__lt = django_filters.NumberFilter(field_name='variants__price', lookup_expr='lte', distinct=True)
    status = django_filters.CharFilter(method='filter_status', )
    order_by = django_filters.CharFilter(method='filter_orderby', )

    def filter_orderby(self, queryset, field_name, value):
        query = queryset
        if value == 'date':
            query = query.order_by('-id')
        elif value == 'price-desc':
            query = query.order_by('-variants__price')
        elif value == 'price':
            query = query.order_by('variants__price')
        return query

    def filter_status(self, queryset, field_name, value):
        values = value.split('-')
        query = queryset
        if 'instock' in values:
            query = query.filter(variants__stock__gt=0).distinct()
        elif 'onsale' in values:
            query = query.filter(discount_start_date__lte=datetime.now().date(), discount_end_date__gt=datetime.now().date()).distinct()
        return query

    class Meta:
        model = Product
        fields = ('category', )
