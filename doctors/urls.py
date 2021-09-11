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
    path("password_reset/", views.password_reset_view, name="password_reset_view"),
    path(
        "validate_email/",
        csrf_exempt(views.validate_email_for_doctors_password_reset),
        name="validate_email_for_doctors_password_reset",
    ),
    path(
        "send_otp_via_email/",
        csrf_exempt(views.send_otp_via_email_view),
        name="send_otp_via_email_view",
    ),
    path(
        "doctors_password_reset_view/",
        csrf_exempt(views.doctors_password_reset_view),
        name="doctors_password_reset_view",
    ),
    path("doctors_list/", views.doctors_list_view.as_view(), name="doctors_list_view"),
    path("doctors_profile/", views.doctors_profile_view, name="doctors_profile_view"),
    path(
        "account_update/<slug:pk>",
        views.account_update_view.as_view(),
        name="account_update_view",
    ),
    path(
        "add_blog/",
        views.add_blog_view.as_view(),
        name="add_blog_view",
    ),
    path(
        "blog_list/",
        views.blog_list_view.as_view(),
        name="blog_list_view",
    ),
    path(
        "update_blog/<slug:pk>",
        views.update_blog_view.as_view(),
        name="update_blog_view",
    ),
    path(
        "appointment_list/",
        views.appointment_list_view,
        name="appointment_list_view",
    ),
    path(
        "approve_appointment_view/",
        csrf_exempt(views.approve_appointment_view),
        name="approve_appointment_view",
    ),
    path(
        "decline_appointment_view/",
        csrf_exempt(views.decline_appointment_view),
        name="decline_appointment_view",
    ),
    path(
        "verefy_schedule_view/",
        csrf_exempt(views.verefy_schedule_view),
        name="verefy_schedule_view",
    ),
    path(
        "reschedule_appointment_view/",
        csrf_exempt(views.reschedule_appointment_view),
        name="reschedule_appointment_view",
    ),
    path(
        "archived_appointment_list_view/",
        views.archived_appointment_list_view,
        name="archived_appointment_list_view",
    ),
    path(
        "delete_appointment_view/",
        csrf_exempt(views.delete_appointment_view),
        name="delete_appointment_view",
    ),
    path(
        "checkup/",
        views.checkup_view,
        name="checkup_view",
    ),
    path(
        "checkup_result_and_history/",
        views.checkup_result_and_history_view,
        name="checkup_result_and_history_view",
    ),
    path(
        "view_checkup_result_history/",
        views.view_checkup_result_history_view,
        name="view_checkup_result_history_view",
    ),
]
