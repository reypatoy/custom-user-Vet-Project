from django.urls import path
from django.contrib.auth import logout, login

from . import views

app_name = 'staff'


urlpatterns = [
    path('dashboard/', views.staff_dashboard_view, name='staff_dashboard_view'),
    path('login/', views.staff_login_view, name='staff_login_view'),
    path('logout/', views.staff_logout_view, name='staff_logout_view'),
    path('add_pet/', views.add_pet_view.as_view(), name='add_pet_view'),
    path('add_staff/', views.add_staff_view, name='add_staff_view'),
    path('pets_list/', views.pets_list_view.as_view(), name="pets_list_view"),
    path('staff_list/', views.staff_list_view.as_view(), name="staff_list_view"),
    path('staff_update/<slug:pk>', views.staff_update_view.as_view(),
         name="staff_update_view"),
    path('staff_profile/', views.staff_profile_view, name="staff_profile_view"),
    path('customers_list', views.customers_list_view.as_view(),
         name="customers_list_view"),
    path('customers_profile/', views.customers_profile_view,
         name="customers_profile_view"),
    path('add_pet_for_customer/<slug:pk>', views.add_pet_specific_customer_view.as_view(),
         name="add_pet_specific_customer_view"),
    path('pet_update/<slug:pk>', views.pet_update_view.as_view(),
         name="pet_update_view"),
    path('add_customer/', views.add_customer_view.as_view(),
         name="add_customer_view"),

]
