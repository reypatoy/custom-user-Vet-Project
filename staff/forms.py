from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, staff
from django import forms
from django.forms import fields


class add_staff_form(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    profile_pic = forms.ImageField(required=True)
    address_barangay = forms.CharField(max_length=100, required=True)
    address_municipality = forms.CharField(max_length=100, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(max_length=50, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'address_barangay', 'profile_pic', 'address_municipality', 'contact_number',
                  'email', 'username', 'password1', 'password2', 'user_type')
