from django.db import models
from django.db.models.base import Model

# Create your models here.
from accounts.models import Admin


class Blogs(models.Model):
    id = models.IntegerField(primary_key=True)
    blog_title = models.CharField(max_length=255, null=True, blank=True)
    blog_description = models.CharField(max_length=255, null=True, blank=True)
    blog_image = models.ImageField(
        upload_to="blog_images", default="no_blog_images.jpeg"
    )
    blog_uploader = models.ForeignKey(
        Admin, related_name="blogs", on_delete=models.CASCADE
    )
