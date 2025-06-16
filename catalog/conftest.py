import os 
import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        username='test_user_super', 
        password='password_user_super')