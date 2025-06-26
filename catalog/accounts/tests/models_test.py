import pytest

from accounts.models import User
from products.models import Cart

@pytest.mark.django_db
def test_profile_creation():
    user = User.objects.create_user(username="testuser", password="12345")

    profile = user.profile

    cart, _ = Cart.objects.get_or_create(user=user)

    assert profile.avatar.name == 'avatars/' 
    assert profile.user == user
    assert cart.user == user