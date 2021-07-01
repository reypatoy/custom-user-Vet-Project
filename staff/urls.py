from django.urls import path
from django.contrib.auth import logout, login

from .views import staff_dashboard_view, staff_login_view, staff_logout_view, add_pet_view

app_name = 'staff'


urlpatterns = [
    path('dashboard/', staff_dashboard_view, name='staff_dashboard_view'),
    path('login/', staff_login_view, name='staff_login_view'),
    path('logout/', staff_logout_view, name='staff_logout_view'),
    path('add_pet/', add_pet_view, name='add_pet_view')

]
