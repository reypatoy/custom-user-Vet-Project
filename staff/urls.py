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
    path('pets_list/', views.pets_list_view.as_view(), name="pets_list_view")
]
