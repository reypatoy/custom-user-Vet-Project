from functools import WRAPPER_ASSIGNMENTS
from django.db import models

# Create your models here.
from accounts.models import customer


class pets(models.Model):
    pet_name = models.CharField(max_length=200)
    breed = models.CharField(max_length=200)
    age = models.IntegerField()
    owner = models.ForeignKey(
        customer, verbose_name='owner', on_delete=models.SET_DEFAULT, default=3)

    def __str__(self):
        return self.pet_name
