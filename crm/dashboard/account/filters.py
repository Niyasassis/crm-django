import django_filters

from .models import *

from django_filters import DateFilter


class Orderfilters(django_filters.FilterSet):
    note = DateFilter(field_name='note',lookup_expr='icontains')
    class Meta:
        model = Order
        fields ='__all__'
        exclude = ['customer', 'date_created']