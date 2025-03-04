from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer, CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления корзиной пользователя.

    Позволяет авторизованным пользователям:
    - Добавлять продукты в корзину.
    - Изменять количество продуктов в корзине.
    - Удалять продукты из корзины.
    - Очищать корзину.
    - Просматривать содержимое корзины
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).order_by('id')

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Добавляет продукт в корзину."""
        cart = self.get_queryset().first()
        product_name = request.data.get('product_name')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, name=product_name)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """
        Обновляет количество продукта в корзине.
        """
        cart = self.get_queryset().first()
        product_name = request.data.get('product_name')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, name=product_name)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        if quantity <= 0:
            cart_item.delete()
            return Response({f'Продукт {product_name} удален из корзины.'})
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Удаляет продукт из корзины."""
        cart = self.get_queryset().first()
        product_name = request.data.get('product_name')
        product = get_object_or_404(Product, name=product_name)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()
        return Response({f'Продукт {product_name} удален из корзины.'})

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Очищает корзину пользователя."""
        cart = self.get_queryset().first()
        cart.items.all().delete()
        return Response({'Корзина очищена'})


def index(request):
    return render(request, 'index.html')