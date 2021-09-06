from django.db import models
from django.db.models.fields import TextField

# Create your models here.
from pets.models import pets
from accounts.models import Admin


class Checkup(models.Model):
    id = models.IntegerField(primary_key=True)
    pet = models.ForeignKey(pets, related_name="checkup", on_delete=models.CASCADE)
    what_is_your_pet_coming_in_for_today = models.CharField(max_length=255, null=True)
    how_long_have_the_problem_been_going_on = models.CharField(max_length=255,null=True)
    has_your_pet_had_any_choices = (
        (1, "Vomiting"),
        (2, "Diarrhea"),
        (3, "Coughing"),
        (4, "Sneezing"),
    )
    has_your_pet_had_any = models.IntegerField(choices=has_your_pet_had_any_choices)
    general_choices = ((1, "Normal"), (2, "Increased"), (3, "Decreased"), (4, "None"))
    pets_appetite = models.IntegerField(choices=general_choices)
    drinking = models.IntegerField(choices=general_choices)
    urination = models.IntegerField(choices=general_choices)
    activity_level = models.IntegerField(choices=general_choices)
    vaccination_choices = ((1, "Rabies"), (2, "C6"), (3, "C6/CV"), (4, "Pneumodog"))
    vaccination = models.IntegerField(choices=vaccination_choices)
    deworming_choices = ((1, "GI worms"), (2, "Heartworm Prevention"))
    deworming = models.IntegerField(choices=deworming_choices)
    tick_and_flea_tx = models.CharField(max_length=255, null=True)
    endoctocide = models.CharField(max_length=255, null=True)
    what_does_your_pet_eat = models.CharField(max_length=255, null=True)
    when_did_your_pet_last_eat = models.DateTimeField(null=True)
    is_your_pet_taking_any_medications_choices = ((1, "Yes"), (2, "No"))
    is_your_pet_taking_any_medications = models.IntegerField(
        choices=is_your_pet_taking_any_medications_choices
    )
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
