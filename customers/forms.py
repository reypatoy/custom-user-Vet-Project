from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import EmailField
from accounts.models import User
from appointments.models import Appointment
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    profile_pic = forms.ImageField(required=True)
    contact_number = forms.IntegerField(max_value=None, required=True)
    address_barangay = forms.CharField(max_length=200, required=True)
    address_municipality = forms.CharField(max_length=200, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "profile_pic",
            "contact_number",
            "address_barangay",
            "address_municipality",
            "email",
            "password1",
            "password2",
            "user_type",
        )
