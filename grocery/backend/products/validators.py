from rest_framework import serializers

from .models import Category, SubCategory


def validate_category_name(value):
    """ Проверка, что категория с таким именем существует. """
    if not Category.objects.filter(name=value).exists():
        raise serializers.ValidationError(
            "Категория с таким именем не найдена."
        )
    return value


def validate_subcategory_name(value):
    """
    Проверка, что подкатегория с таким именем существует.
    """
    if not SubCategory.objects.filter(name=value).exists():
        raise serializers.ValidationError(
            "Подкатегория с таким именем не найдена."
        )
    return value


def validate_unique_name(model, name):
    """ Проверка, что имя уникально для заданной модели. """
    if model.objects.filter(name=name).exists():
        raise serializers.ValidationError(
            f"{model.__name__} с таким именем уже существует."
        )
    return name


def validate_unique_slug(model, slug):
    """ Проверка, что slug уникален для заданной модели. """
    if model.objects.filter(slug=slug).exists():
        raise serializers.ValidationError(
            f"{model.__name__} с таким slug уже существует."
        )
    return slug


def validate_positive_price(value):
    """ Проверка, что цена положительная. """
    if value <= 0:
        raise serializers.ValidationError(
            "Цена должна быть положительным числом."
        )
    return value
