# Generated by Django 3.2.4 on 2021-08-12 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_alter_blogs_blog_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='blog_description',
            new_name='illness_description',
        ),
        migrations.RenameField(
            model_name='blogs',
            old_name='blog_image',
            new_name='illness_image',
        ),
        migrations.RenameField(
            model_name='blogs',
            old_name='blog_title',
            new_name='illness_name',
        ),
        migrations.RenameField(
            model_name='blogs',
            old_name='blog_uploader',
            new_name='illness_uploader',
        ),
        migrations.AddField(
            model_name='blogs',
            name='illness_prevention',
            field=models.TextField(blank=True, null=True),
        ),
    ]
