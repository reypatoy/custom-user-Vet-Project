# Generated by Django 3.2.4 on 2021-07-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='added_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
