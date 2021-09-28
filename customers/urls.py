from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


from .views import (
    home_view,
    signup_view,
    login_view,
    profile_view,
    logout_view,
    blogs_view,
    appointment_view,
    verefy_schedule_view,
    save_appointment_view,
)

app_name = "customers"

urlpatterns = [
    path("", home_view, name="home_view"),
    path("signup/", signup_view, name="signup_view"),
    path("login/", login_view, name="login_view"),
    path("profile/", profile_view, name="profile_view"),
    path("logout/", logout_view, name="logout_view"),
    path("blogs/", blogs_view, name="blogs_view"),
    path("appointment/", appointment_view, name="appointment_view"),
    path(
        "verefy_schedule/",
        csrf_exempt(verefy_schedule_view),
        name="verefy_schedule_view",
    ),
    path(
        "save_appointment/",
        csrf_exempt(save_appointment_view),
        name="save_appointment_view",
    ),
]
