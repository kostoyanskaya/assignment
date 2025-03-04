from rest_framework import serializers


def validate_cart_items(items):
    """
    Валидация элементов корзины.
    """
    for item in items:
        if not isinstance(item, dict):
            raise serializers.ValidationError(
                "Каждый элемент корзины должен быть словарем."
            )

        if 'product_name' not in item or 'quantity' not in item:
            raise serializers.ValidationError(
                "Элемент должен содержать 'product_name' и 'quantity'."
            )

        if not isinstance(item['product_name'], str):
            raise serializers.ValidationError(
                "Название продукта должно быть строкой."
            )

        if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
            raise serializers.ValidationError(
                "Количество продукта должно быть положительным целым числом."
            )

    return items
