# Generated by Django 3.2.4 on 2021-08-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0011_rename_pet_id_pets_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pets',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
