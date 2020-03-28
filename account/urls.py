from django.urls import path, include
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="login"),
    path("account", include('allauth.urls')),
    path("charte", views.charte, name="charte"),
]
