import pytest

from accounts.models import Profile, User
from products.models import Cart

@pytest.mark.django_db
def test_profile_creation():
    user = User.objects.create_user(username="testuser", password="12345")
    profile = Profile.objects.create(user=user)
    
    cart, _ = Cart.objects.get_or_create(user=user)

    assert profile.avatar == 'media/avatars/images.png'
    assert profile.user == user
    assert cart.user == user