# Generated by Django 3.2.4 on 2021-08-12 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_uploader',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
