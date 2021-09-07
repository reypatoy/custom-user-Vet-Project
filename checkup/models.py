from django.db import models
from django.db.models.fields import TextField

# Create your models here.
from pets.models import pets
from accounts.models import Admin


class Checkup(models.Model):
    id = models.IntegerField(primary_key=True)
    pet = models.ForeignKey(pets, related_name="checkup", on_delete=models.CASCADE)
    what_is_your_pet_coming_in_for_today = models.CharField(max_length=255, null=True)
    how_long_have_the_problem_been_going_on = models.CharField(
        max_length=255, null=True
    )
    has_your_pet_had_any = models.CharField(max_length=255, null=True)
    pets_appetite = models.CharField(max_length=255, null=True)
    drinking = models.CharField(max_length=255, null=True)
    urination = models.CharField(max_length=255, null=True)
    activity_level = models.CharField(max_length=255, null=True)
    vaccination = models.CharField(max_length=255, null=True)
    deworming = models.CharField(max_length=255, null=True)
    tick_and_flea_tx = models.CharField(max_length=255, null=True)
    endoctocide = models.CharField(max_length=255, null=True)
    what_does_your_pet_eat = models.CharField(max_length=255, null=True)
    when_did_your_pet_last_eat = models.CharField(max_length=255, null=True)
    is_your_pet_taking_any_medications = models.CharField(max_length=255, null=True)
    if_so_please_list_medication_and_doses = models.CharField(max_length=255, null=True)
    body_weight = models.CharField(max_length=255, null=True)
    temparature = models.CharField(max_length=255, null=True)
    heart_rate = models.CharField(max_length=255, null=True)
    respiratory_rate = models.CharField(max_length=255, null=True)
    mm = models.CharField(max_length=255, null=True)
    crt_sec = models.CharField(max_length=255, null=True)
    dehydration_nms = models.CharField(max_length=255, null=True)
    skin_coat = models.CharField(max_length=255, null=True)
    discharge_nose_eye_vulva_etc = models.CharField(max_length=255, null=True)
    others = models.CharField(max_length=255, null=True)
    diff_dx = models.CharField(max_length=255, null=True)
    laboratory = models.CharField(max_length=255, null=True)
    definitive_dx = models.CharField(max_length=255, null=True)
    prognosis = models.CharField(max_length=255, null=True)
    tx = models.TextField(null=True)
    rx = models.TextField(null=True)
    attending_veterinarian = models.ForeignKey(
        Admin, related_name="checkup", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
