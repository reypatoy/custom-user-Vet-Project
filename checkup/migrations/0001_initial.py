# Generated by Django 3.2.4 on 2021-09-06 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pets', '0012_alter_pets_id'),
        ('accounts', '0011_auto_20210811_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('what_is_your_pet_coming_in_for_today', models.CharField(max_length=255, null=True)),
                ('how_long_have_the_problem_been_going_on', models.CharField(max_length=255, null=True)),
                ('has_your_pet_had_any', models.IntegerField(choices=[(1, 'Vomiting'), (2, 'Diarrhea'), (3, 'Coughing'), (4, 'Sneezing')])),
                ('pets_appetite', models.IntegerField(choices=[(1, 'Normal'), (2, 'Increased'), (3, 'Decreased'), (4, 'None')])),
                ('drinking', models.IntegerField(choices=[(1, 'Normal'), (2, 'Increased'), (3, 'Decreased'), (4, 'None')])),
                ('urination', models.IntegerField(choices=[(1, 'Normal'), (2, 'Increased'), (3, 'Decreased'), (4, 'None')])),
                ('activity_level', models.IntegerField(choices=[(1, 'Normal'), (2, 'Increased'), (3, 'Decreased'), (4, 'None')])),
                ('vaccination', models.IntegerField(choices=[(1, 'Rabies'), (2, 'C6'), (3, 'C6/CV'), (4, 'Pneumodog')])),
                ('deworming', models.IntegerField(choices=[(1, 'GI worms'), (2, 'Heartworm Prevention')])),
                ('tick_and_flea_tx', models.CharField(max_length=255, null=True)),
                ('endoctocide', models.CharField(max_length=255, null=True)),
                ('what_does_your_pet_eat', models.CharField(max_length=255, null=True)),
                ('when_did_your_pet_last_eat', models.DateTimeField(null=True)),
                ('is_your_pet_taking_any_medications', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')])),
                ('if_so_please_list_medication_and_doses', models.CharField(max_length=255, null=True)),
                ('body_weight', models.CharField(max_length=255, null=True)),
                ('temparature', models.CharField(max_length=255, null=True)),
                ('heart_rate', models.CharField(max_length=255, null=True)),
                ('respiratory_rate', models.CharField(max_length=255, null=True)),
                ('mm', models.CharField(max_length=255, null=True)),
                ('crt_sec', models.CharField(max_length=255, null=True)),
                ('dehydration_nms', models.CharField(max_length=255, null=True)),
                ('skin_coat', models.CharField(max_length=255, null=True)),
                ('discharge_nose_eye_vulva_etc', models.CharField(max_length=255, null=True)),
                ('others', models.CharField(max_length=255, null=True)),
                ('diff_dx', models.CharField(max_length=255, null=True)),
                ('laboratory', models.CharField(max_length=255, null=True)),
                ('definitive_dx', models.CharField(max_length=255, null=True)),
                ('prognosis', models.CharField(max_length=255, null=True)),
                ('tx', models.TextField(null=True)),
                ('rx', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attending_veterinarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkup', to='accounts.admin')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkup', to='pets.pets')),
            ],
        ),
    ]