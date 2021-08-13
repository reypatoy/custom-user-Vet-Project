from django.db import models
from django.db.models.base import Model

# Create your models here.
from accounts.models import User


class Blogs(models.Model):
    id = models.IntegerField(primary_key=True)
    illness_name = models.CharField(max_length=255, null=True, blank=True)
    illness_description = models.TextField(null=True, blank=True)
    illness_image = models.ImageField(
        upload_to="blog_images", default="no_blog_images.jpeg"
    )
    illness_uploader = models.ForeignKey(
        User,
        related_name="blogs",
        max_length=255,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    illness_prevention = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
