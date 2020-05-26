# Generated by Django 2.1.8 on 2020-05-26 12:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200526_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickupnotification',
            name='notif_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='buyinbooking',
            name='buy_in_id',
            field=models.UUIDField(default=uuid.UUID('153fc8aa-24b8-464f-ae72-126c27fe7674'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pickupbooking',
            name='pick_up_id',
            field=models.UUIDField(default=uuid.UUID('dd277460-e5ac-430d-9079-fe66fe116b69'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='slot',
            name='slot_id',
            field=models.UUIDField(default=uuid.UUID('bbfd0e36-86ce-433c-91de-a30c318610b0'), editable=False, primary_key=True, serialize=False),
        ),
    ]
