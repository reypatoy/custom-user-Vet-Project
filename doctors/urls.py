from django.urls import path


from . import views

app_name = 'doctors'

urlpatterns = [
    path('login/', views.doctors_login_view, name="doctors_login_view"),
]
