import pytest
import uuid

from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal

from products.models import Product
from .fixtures import *

@pytest.mark.django_db
def test_product_list(api_client):
    url = reverse('products:products-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_product_list(api_client, product, product_with_discount):
    url = reverse('products:products-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_product_list(api_client, product, product_with_discount):
    url = reverse('products:products-detail', kwargs={'pk':product.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == product.name


@pytest.mark.django_db
def test_product_detail_not_found(api_client):
    url = reverse('products:products-detail', kwargs={'pk': 124312})

    responce = api_client.get(url)

    assert responce.status_code == 404


@pytest.mark.django_db
def test_update_product_not_authorized(api_client, product):
    url = reverse('products:products-detail', kwargs={'pk': product.id})

    responce = api_client.patch(url, data = {"price"}, format='json')

    assert responce.status_code == 403


@pytest.mark.django_db
def test_update_product(api_client, product, super_user):
    api_client.force_authenticate(super_user)
    url = reverse('products:products-detail', kwargs={'pk': product.id})

    response = api_client.patch(url, data={"price": "100.00"}, format='json')

    assert response.status_code == 200
    assert Decimal(response.data.get("price")) == Decimal("100.00")

    product.refresh_from_db()
    assert product.price == Decimal("100.00")


@pytest.mark.django_db
def test_create_product(api_client, category, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("products:products-list")
    data = {
        "name": "test_name",
        "description": "test_description",
        "category": category.id,
        "nomenclature": str(uuid.uuid4()),
        "price": "100.00",
    }

    response = api_client.post(url, data=data, format='json')

    assert response.status_code == 201
    assert response.data.get('name') == "test_name"
    assert Product.objects.filter(id=response.data.get("id")).exists()