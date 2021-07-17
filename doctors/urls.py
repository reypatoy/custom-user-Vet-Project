from django.urls import path


from . import views

app_name = 'doctors'

urlpatterns = [
    path('login/', views.doctors_login_view, name="doctors_login_view"),
    path('doctors_dashboard/', views.doctors_dashboard_view,
         name="doctors_dashboard_view"),
]
