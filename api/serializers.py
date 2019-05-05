from rest_framework import serializers
from products.models import Product, Category
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            if isinstance(data, int):
                return self.get_queryset().get(pk=data)
            if isinstance(data, str):
                return self.get_queryset().get(name=data)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            self.fail(str(e))
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


class ProductSerializer(serializers.ModelSerializer):
    categories = CategoryField(
        many=True, queryset=Category.objects.all(), read_only=False)

    class Meta:
        model = Product
        fields = '__all__'
