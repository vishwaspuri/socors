# Generated by Django 2.1.8 on 2020-05-22 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200520_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneotp',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
