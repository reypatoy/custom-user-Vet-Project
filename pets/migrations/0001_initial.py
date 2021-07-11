# Generated by Django 3.2.4 on 2021-07-03 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(blank=True, max_length=200, null=True)),
                ('breed', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('owner', models.CharField(blank=True, max_length=100, null=True)),
                ('added_by', models.CharField(blank=True, max_length=100, null=True)),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.customer', verbose_name='Owner Id')),
            ],
        ),
    ]
