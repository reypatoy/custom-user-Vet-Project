from django.urls import path


from . import views

app_name = 'doctors'

urlpatterns = [
    path('login/', views.doctors_login_view, name="doctors_login_view"),
    path('doctors_dashboard/', views.doctors_dashboard_view,
         name="doctors_dashboard_view"),
    path('doctors_logout/', views.doctors_logout_view, name="doctors_logout_view"),
    path('pets_list/', views.pets_list_view.as_view(), name="pets_list_view"),
    path('add_pet/', views.add_pet_view.as_view(), name="add_pet_view"),
    path('pet_update/<slug:pk>', views.update_pet.as_view(), name="update_pet"),
    path('customers_list/',views.customers_list.as_view(),name="customers_list_view"),
]
