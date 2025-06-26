from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from accounts.views.views import (
    register,
    login_view,
    logout_view,
    profile_view,
    edit_profle_view,
    confirm_email_view,
)

app_name = "accounts"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profle_view, name='edit_profile'),

    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("accounts:password_change_done"),
            template_name="password_change.html"
        ),
        name="password_change"
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),

    path("confirm_email/", confirm_email_view, name="confirm_email"),

    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset/form.html",
            email_template_name="password_reset/email.html",
            success_url=reverse_lazy("accounts:password_reset_done")
        ),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset/confirm.html"
        ),
        name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/complete.html"
        ),
        name="password_reset_complete"
    ),
]
