# Generated by Django 2.1.8 on 2020-05-24 05:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_type',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(6)]),
        ),
    ]
