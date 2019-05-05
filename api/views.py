from rest_framework import viewsets
from products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters import rest_framework as djangofilters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(detail=False, methods=['get'])
    def category_tree(self, request):
        root_categories = Category.objects.filter(parent_category=None)
        tree = [{'id': category.id,
                 'name': category.name,
                 'sub_categories': category.get_sub_categories()}
                for category in root_categories]
        return Response(tree, status=status.HTTP_200_OK)


class ProductFilter(djangofilters.FilterSet):
    category = djangofilters.CharFilter(
        field_name="categories__name")

    class Meta:
        model = Product
        fields = ('name', 'product_code', 'category',)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('product_code', 'name', 'categories__name',)
    filterset_class = ProductFilter
