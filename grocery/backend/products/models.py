from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(
        unique=True, blank=True, verbose_name='Уникальный слаг'
    )
    image = models.ImageField(
        upload_to='categories/', verbose_name='Изображение категории'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название подкатегории'
    )
    slug = models.SlugField(
        unique=True, blank=True, verbose_name='Уникальный слаг'
    )
    image = models.ImageField(
        upload_to='subcategories/', verbose_name='Изображение подкатегории'
    )
    category = models.ForeignKey(
        Category, related_name='subcategories',
        on_delete=models.CASCADE, verbose_name='Категория'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название продукта')
    slug = models.SlugField(
        unique=True, blank=True, verbose_name='Уникальный слаг'
    )
    subcategory = models.ForeignKey(
        SubCategory, related_name='products',
        on_delete=models.CASCADE, verbose_name='Подкатегория'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена продукта'
    )
    image_small = models.ImageField(
        upload_to='products/small/', verbose_name='Маленькое изображение'
    )
    image_medium = models.ImageField(
        upload_to='products/medium/', verbose_name='Среднее изображение'
    )
    image_large = models.ImageField(
        upload_to='products/large/', verbose_name='Большое изображение'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
