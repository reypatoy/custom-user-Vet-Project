# Generated by Django 3.2.4 on 2021-07-14 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210713_1735'),
        ('pets', '0005_alter_pets_owner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pets',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pets', to='accounts.customer'),
        ),
    ]