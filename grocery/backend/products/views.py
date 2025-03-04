from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Product, SubCategory
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    SubCategorySerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления категориями.

    Позволяет:
    - Создавать, редактировать и удалять категории.
    - Просматривать список всех категорий с подкатегориями.
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления подкатегориями.

    Позволяет:
    - Создавать, редактировать и удалять подкатегории.
    - Просматривать список всех подкатегорий.
    """
    queryset = SubCategory.objects.all().order_by('id')
    serializer_class = SubCategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления продуктами.

    Позволяет:
    - Создавать, редактировать и удалять продукты.
    - Просматривать список всех продуктов с пагинацией.
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        serializer = self.get_serializer(product)
        return Response(serializer.data)
