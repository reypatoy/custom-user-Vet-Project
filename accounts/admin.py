from django.contrib import admin
from django.db import models

from .models import User, Admin, staff, customer
# Register your models here.


class admin_display(admin.ModelAdmin):
    fieldsets = [
        ('Details', {'fields': ['first_name', 'last_name']})
    ]


admin.site.register(User)
admin.site.register(Admin, admin_display)
admin.site.register(staff)
admin.site.register(customer)
