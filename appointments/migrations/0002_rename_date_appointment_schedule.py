# Generated by Django 3.2.4 on 2021-08-21 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='date',
            new_name='schedule',
        ),
    ]
