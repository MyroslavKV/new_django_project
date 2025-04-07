from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import register, login_view, logout_view, profile_view

app_name = "accounts"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password_change/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy("accounts:password_change_done"),template_name="password_change.html"),name="password_change"),  
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
]