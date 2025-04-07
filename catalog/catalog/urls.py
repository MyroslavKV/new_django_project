from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include("products.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("captcha/", include("captcha.urls"))
]
