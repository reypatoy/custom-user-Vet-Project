from django.db import models

# Create your models here.
from accounts.models import customer


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    schedule = models.DateTimeField(null=True)
    customer = models.ForeignKey(
        customer, related_name="appointment", on_delete=models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)
    status_choices = ((1, "Approve"), (2, "Declined"))
    status = models.IntegerField(choices=status_choices, null=True, blank=True)
