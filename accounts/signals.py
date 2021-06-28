from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Admin, staff, customer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(auth_user_id=instance)
        if instance.user_type == 2:
            staff.objects.create(auth_user_id=instance)
        if instance.user_type == 3:
            customer.objects.create(auth_user_id=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.customer.save()
