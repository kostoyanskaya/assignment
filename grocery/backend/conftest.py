import pytest

from django.contrib.auth import get_user_model

from cart.models import Cart, CartItem
from products.models import Category, Product, SubCategory


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser', password='testpass123'
    )


@pytest.fixture
def category():
    return Category.objects.create(name='Колбасы', slug='Kolbasy')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(
        name='копченые', slug='kopchenye', category=category
    )


@pytest.fixture
def product(subcategory):
    return Product.objects.create(
        name='Итальянские',
        slug='Italyanskie',
        subcategory=subcategory,
        price=100.00
    )


@pytest.fixture
def cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=2)
