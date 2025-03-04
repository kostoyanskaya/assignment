import pytest
from rest_framework.test import APIClient

from cart.models import CartItem


@pytest.mark.django_db
def test_get_cart_authenticated(user, cart, cart_item):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/cart/')
    assert response.status_code == 200
    assert 'results' in response.data
    assert len(response.data['results']) > 0
    first_result = response.data['results'][0]
    assert 'items' in first_result
    expected_items_count = CartItem.objects.filter(cart=cart).count()
    assert len(first_result['items']) == expected_items_count


@pytest.mark.django_db
def test_get_cart_unauthenticated():
    client = APIClient()

    response = client.get('/api/cart/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_add_item_to_cart(user, cart, product):
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "product_name": "Итальянские",
        "quantity": 3
    }
    response = client.post('/api/cart/add_item/', data, format='json')
    assert response.status_code == 200
    assert response.data['quantity'] == 3
    assert CartItem.objects.filter(cart=cart, product=product).exists()


@pytest.mark.django_db
def test_add_item_invalid_data(user):
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "product_name": "Несуществующий продукт",
        "quantity": 3
    }
    response = client.post('/api/cart/add_item/', data, format='json')
    assert response.status_code == 404
