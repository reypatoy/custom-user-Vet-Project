from django.contrib import admin
from django.urls import path, include


from .views import signup_view

app_name = 'customers'

urlpatterns = [
    path('signup/', signup_view, name='signup_view')
]
