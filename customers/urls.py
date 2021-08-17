from django.contrib import admin
from django.urls import path, include


from .views import (
    home_view,
    signup_view,
    login_view,
    dashboard_view,
    logout_view,
    blogs_view,
)

app_name = "customers"

urlpatterns = [
    path("", home_view, name="home_view"),
    path("signup/", signup_view, name="signup_view"),
    path("login/", login_view, name="login_view"),
    path("dashboard/", dashboard_view, name="dashboard_view"),
    path("logout/", logout_view, name="logout_view"),
    path("blogs/", blogs_view, name="blogs_view"),
]
