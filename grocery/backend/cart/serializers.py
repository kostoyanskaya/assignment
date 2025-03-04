from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Cart, CartItem
from .validators import validate_cart_items
from products.models import Product
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для элементов корзины."""
    product_name = serializers.CharField(write_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity']

    def create(self, validated_data):
        product_name = validated_data.pop('product_name')
        product = get_object_or_404(Product, name=product_name)
        validated_data['product'] = product
        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины."""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items']

    @extend_schema_field(
            serializers.DecimalField(max_digits=10, decimal_places=2)
        )
    def get_total_price(self, obj):
        return sum(
            item.product.price * item.quantity for item in obj.items.all()
        )

    @extend_schema_field(serializers.IntegerField())
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def create(self, validated_data):
        user = self.context['request'].user
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError("У вас уже есть корзина.")
        return super().create(validated_data)

    def validate_items(self, items):
        """
        Валидация элементов корзины.
        """
        return validate_cart_items(items)
