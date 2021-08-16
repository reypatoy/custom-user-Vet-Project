from django.urls import path
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "staff"


urlpatterns = [
    path("dashboard/", views.staff_dashboard_view, name="staff_dashboard_view"),
    path("login/", views.staff_login_view, name="staff_login_view"),
    path("logout/", views.staff_logout_view, name="staff_logout_view"),
    path("add_pet/", views.add_pet_view.as_view(), name="add_pet_view"),
    path("add_staff/", views.add_staff_view, name="add_staff_view"),
    path("pets_list/", views.pets_list_view.as_view(), name="pets_list_view"),
    path("staff_list/", views.staff_list_view.as_view(), name="staff_list_view"),
    path(
        "staff_update/<slug:pk>",
        views.staff_update_view.as_view(),
        name="staff_update_view",
    ),
    path("staff_profile/", views.staff_profile_view, name="staff_profile_view"),
    path(
        "customers_list/",
        views.customers_list_view.as_view(),
        name="customers_list_view",
    ),
    path(
        "customers_profile/",
        views.customers_profile_view,
        name="customers_profile_view",
    ),
    path(
        "add_pet_for_customer/<slug:pk>",
        views.add_pet_specific_customer_view.as_view(),
        name="add_pet_specific_customer_view",
    ),
    path(
        "pet_update/<slug:pk>",
        views.pet_update_view.as_view(),
        name="pet_update_view",
    ),
    path("add_customer/", views.add_customer_view.as_view(), name="add_customer_view"),
    path("sent_email/", csrf_exempt(views.send_email_view), name="send_email_view"),
    path("password_reset/", views.password_reset_view, name="password_reset_view"),
    path(
        "validate_email/",
        csrf_exempt(views.validate_email_for_staff_password_reset),
        name="validate_email_for_staff_password_reset",
    ),
    path(
        "send_otp_via_email/",
        csrf_exempt(views.send_otp_via_email_view),
        name="send_otp_via_email_view",
    ),
    path(
        "staff_password_reset_view/",
        csrf_exempt(views.staff_password_reset_view),
        name="staff_password_reset_view",
    ),
    path(
        "account_update/<slug:pk>",
        views.account_update_view.as_view(),
        name="account_update_view",
    ),
    path(
        "blog_list/",
        views.blog_list_view.as_view(),
        name="blog_list_view",
    ),
    path("doctors_list/", views.doctors_list_view.as_view(), name="doctors_list_view"),
     path("doctors_profile/", views.doctors_profile_view, name="doctors_profile_view"),
]
