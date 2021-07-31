from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "doctors"

urlpatterns = [
    path("login/", views.doctors_login_view, name="doctors_login_view"),
    path(
        "doctors_dashboard/",
        views.doctors_dashboard_view,
        name="doctors_dashboard_view",
    ),
    path("doctors_logout/", views.doctors_logout_view, name="doctors_logout_view"),
    path("pets_list/", views.pets_list_view.as_view(), name="pets_list_view"),
    path("add_pet/", views.add_pet_view.as_view(), name="add_pet_view"),
    path("pet_update/<slug:pk>", views.update_pet.as_view(), name="update_pet"),
    path("customers_list/", views.customers_list.as_view(), name="customers_list_view"),
    path("add_customer/", views.add_customer_view.as_view(), name="add_customer_view"),
    path(
        "customer_profile/", views.customer_profile_view, name="customer_profile_view"
    ),
    path(
        "add_pet_specific_customer/<slug:pk>",
        views.add_pet_specific_customer_view.as_view(),
        name="add_pet_specific_customer_view",
    ),
    path("staff_list/", views.staff_list_view.as_view(), name="staff_list_view"),
    path("add_staff/", views.add_staff_view.as_view(), name="add_staff_view"),
    path("staff_profile/", views.staff_profile_view, name="staff_profile_view"),
    path("add_doctor/", views.add_doctor_view.as_view(), name="add_doctor_view"),
    path("sent_email/", csrf_exempt(views.send_email_view), name="send_email_view"),
]
