from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='cart', verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания корзины'
    )

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name='items',
        on_delete=models.CASCADE, verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Количество'
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в {self.cart}"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
