import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.accounts.models import Profile, User
from catalog.products.models import Cart

@pytest.mark.django_db
def test_profile_creation():
    user = User.objets.create_user()
    profile = Profile.objects.create(user=user)
    cart = Cart.objects.create(user=user)
    assert profile.avatar == 'avatar/images.png'
    assert profile.user == user
    assert cart.user == user