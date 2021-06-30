from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    User_Type = ((1, 'Admin'), (2, 'Staff'), (3, 'Customer'))
    user_type = models.IntegerField(choices=User_Type, default=1)


class Admin(models.Model):
    profile_pic = models.ImageField(
        upload_to='profile_pictures', default='default_image.png')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address_barangay = models.CharField(max_length=100, blank=True, null=True)
    address_municipality = models.CharField(
        max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_user_id = models.OneToOneField(
        User, related_name='admin', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auth_user_id.first_name} {self.auth_user_id.last_name}"


class staff(models.Model):
    profile_pic = models.ImageField(
        upload_to='profile_pictures', default='default_image.png')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address_barangay = models.CharField(max_length=100, blank=True, null=True)
    address_municipality = models.CharField(
        max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_user_id = models.OneToOneField(
        User, related_name='staff', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auth_user_id.first_name} {self.auth_user_id.last_name}"


class customer(models.Model):
    profile_pic = models.ImageField(
        upload_to='profile_pictures', default='default_image.png')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address_barangay = models.CharField(max_length=100, blank=True, null=True)
    address_municipality = models.CharField(
        max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_user_id = models.OneToOneField(
        User, related_name='customer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auth_user_id.first_name} {self.auth_user_id.last_name}"
