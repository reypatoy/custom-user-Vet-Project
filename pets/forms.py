from django import forms
from django.forms import fields


from .models import pets


class pets_form(forms.Form):
    pets_name = forms.CharField()
    age = forms.IntegerField()
    breed = forms.CharField()

    class meta:
        model = pets
        fields = ('pets_name', 'age', 'breed')
