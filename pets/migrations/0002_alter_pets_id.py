# Generated by Django 3.2.4 on 2021-07-10 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pets',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]