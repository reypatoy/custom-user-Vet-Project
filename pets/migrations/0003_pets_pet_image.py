# Generated by Django 3.2.4 on 2021-07-10 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_alter_pets_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pets',
            name='pet_image',
            field=models.ImageField(default='default_image.png', upload_to='Pet_images'),
        ),
    ]