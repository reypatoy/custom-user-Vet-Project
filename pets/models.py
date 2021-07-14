from django.db import models
from django.urls import reverse
# Create your models here.
from accounts.models import customer


class pets(models.Model):
    id = models.AutoField(primary_key=True)
    pet_image = models.ImageField(
        upload_to="Pet_images", default="default_image.png")
    pet_name = models.CharField(max_length=200, blank=True, null=True)
    breed = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    added_by = models.CharField(max_length=100, blank=True, null=True)
    owner_id = models.ForeignKey(
        customer, related_name="pets", on_delete=models.SET_NULL, null=True)
    added_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pet_name

    def get_absolute_url(self):
        return reverse("staff:add_pet_view")
