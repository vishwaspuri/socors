# Generated by Django 2.1.8 on 2020-05-26 12:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200526_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyinbooking',
            name='buy_in_id',
            field=models.UUIDField(default=uuid.UUID('6f1c7cb3-0bf9-4752-981d-c231062d0753'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pickupbooking',
            name='pick_up_id',
            field=models.UUIDField(default=uuid.UUID('4f12fd37-b145-4f80-b98f-811a7339c09b'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='slot',
            name='slot_id',
            field=models.UUIDField(default=uuid.UUID('6dfa8b6a-7759-4846-a279-98512a546aa5'), editable=False, primary_key=True, serialize=False),
        ),
    ]
