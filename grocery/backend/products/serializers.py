import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Category, Product, SubCategory
from .validators import (
    validate_category_name,
    validate_positive_price,
    validate_subcategory_name,
    validate_unique_name,
    validate_unique_slug,
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            name = f'temp.{ext}'
            file = ContentFile(base64.b64decode(imgstr), name=name)
            data = file
        return super().to_internal_value(data)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    image = Base64ImageField()

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, attrs):
        """
        Проверка, что имя и slug категории уникальны.
        """
        name = attrs.get('name')
        slug = attrs.get('slug')

        validate_unique_name(Category, name)
        validate_unique_slug(Category, slug)

        return attrs


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""
    image = Base64ImageField()
    category_name = serializers.CharField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')
        slug = attrs.get('slug')
        category_name = attrs.get('category_name')

        validate_unique_name(SubCategory, name)
        validate_unique_slug(SubCategory, slug)
        validate_category_name(category_name)

        return attrs

    def create(self, validated_data):
        category_name = validated_data.pop('category_name')
        category = get_object_or_404(Category, name=category_name)
        validated_data['category'] = category
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""
    image_small = Base64ImageField()
    image_medium = Base64ImageField()
    image_large = Base64ImageField()
    subcategory_name = serializers.CharField(write_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')
        slug = attrs.get('slug')
        subcategory_name = attrs.get('subcategory_name')
        price = attrs.get('price')

        validate_unique_name(Product, name)
        validate_unique_slug(Product, slug)
        validate_subcategory_name(subcategory_name)
        validate_positive_price(price)

        return attrs

    def create(self, validated_data):
        subcategory_name = validated_data.pop('subcategory_name')
        subcategory = get_object_or_404(SubCategory, name=subcategory_name)
        validated_data['subcategory'] = subcategory
        return super().create(validated_data)
