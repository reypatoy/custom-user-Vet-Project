from django.urls import path


from .views import staff_dashboard_view

app_name = 'staff'


urlpatterns = [
    path('dashboard/', staff_dashboard_view, name='staff_dashboard_view')

]
