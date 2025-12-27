from django_filters import rest_framework as filters
from .models import Product, Store

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'lt'],
        }

class StoreFilter(filters.FilterSet):
    class Meta:
        model = Store
        fields = {
            'subcategory': ['exact'],
        }