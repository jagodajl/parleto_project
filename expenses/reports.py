from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.functions import TruncMonth


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_per_year_month(queryset):
    return OrderedDict(sorted(
        queryset.annotate(year_month=TruncMonth('date'), )
        .order_by()
        .values('year_month')
        .annotate(sum=Sum('amount'))
        .values_list('year_month', 'sum')
    ))


def summary_overall(queryset):
    amount_sum = sum([value[0] for value in queryset.values_list('amount')])
    return {'overall': amount_sum}
