from django_filters import rest_framework as filters
from .models import Menu
from django.utils import timezone


class MenuFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="date", lookup_expr='exact')

    class Meta:
        model = Menu
        fields = {'date': ['exact'],
}
