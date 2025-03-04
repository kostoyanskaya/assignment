import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from products.models import Category, SubCategory, Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Load data from JSON files'

    def handle(self, *args, **kwargs):
        self.load_categories()
        self.load_subcategories()
        self.load_products()
        self.load_users()
        self.load_carts()

    def load_categories(self):
        with open('data/categories.json', 'r', encoding='utf-8') as file:
            categories = json.load(file)
            for category_data in categories:
                Category.objects.get_or_create(**category_data)
        self.stdout.write(self.style.SUCCESS('Категории успешно загружены.'))

    def load_subcategories(self):
        with open('data/subcategories.json', 'r', encoding='utf-8') as file:
            subcategories = json.load(file)
            for subcategory_data in subcategories:
                category_name = subcategory_data.pop('category_name')
                category = Category.objects.get(name=category_name)
                SubCategory.objects.get_or_create(category=category, **subcategory_data)
        self.stdout.write(self.style.SUCCESS('Подкатегории успешно загружены.'))

    def load_products(self):
        with open('data/products.json', 'r', encoding='utf-8') as file:
            products = json.load(file)
            for product_data in products:
                subcategory_name = product_data.pop('subcategory_name')
                subcategory = SubCategory.objects.get(name=subcategory_name)
                Product.objects.get_or_create(subcategory=subcategory, **product_data)
        self.stdout.write(self.style.SUCCESS('Продукты успешно загружены.'))

    def load_users(self):
        with open('data/users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
            for user_data in users:
                User.objects.create_user(**user_data)
        self.stdout.write(self.style.SUCCESS('Пользователи успешно загружены.'))

    def load_carts(self):
        with open('data/carts.json', 'r', encoding='utf-8') as file:
            carts = json.load(file)
            for cart_data in carts:
                user = User.objects.get(username=cart_data['user_username'])
                cart, created = Cart.objects.get_or_create(user=user)
                for item_data in cart_data['items']:
                    product = Product.objects.get(name=item_data['product_name'])
                    CartItem.objects.get_or_create(cart=cart, product=product, quantity=item_data['quantity'])
        self.stdout.write(self.style.SUCCESS('Корзины успешно загружены.'))