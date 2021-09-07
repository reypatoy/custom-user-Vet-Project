# Generated by Django 3.2.4 on 2021-09-07 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkup',
            name='activity_level',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='deworming',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='drinking',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='has_your_pet_had_any',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='is_your_pet_taking_any_medications',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='pets_appetite',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='urination',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='vaccination',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checkup',
            name='when_did_your_pet_last_eat',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
