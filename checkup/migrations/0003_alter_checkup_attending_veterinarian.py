# Generated by Django 3.2.4 on 2021-09-09 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210811_1910'),
        ('checkup', '0002_auto_20210907_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkup',
            name='attending_veterinarian',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkup', to='accounts.admin'),
        ),
    ]
