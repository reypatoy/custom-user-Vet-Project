
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    contact_number = forms.IntegerField(max_value=None, required=True)
    address_barangay = forms.CharField(max_length=200, required=True)
    address_municipality = forms.CharField(max_length=200, required=True)
    profile_pic = forms.ImageField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'profile_pic', 'contact_number', 'address_barangay',
            'address_municipality', 'username', 'password1', 'password2', 'user_type'
        )
