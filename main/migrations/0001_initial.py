# Generated by Django 2.1.8 on 2020-05-24 13:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_message', models.BooleanField(default=False)),
                ('message_for_shopkeeper', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_name', models.CharField(max_length=60)),
                ('gst_id', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('start_time', models.TimeField()),
                ('stop_time', models.TimeField()),
                ('shop_capacity', models.IntegerField()),
                ('owner_name', models.CharField(max_length=120)),
                ('owner_phone_number', models.CharField(max_length=10)),
                ('shop_pincode', models.IntegerField(validators=[django.core.validators.MaxValueValidator(999999)])),
                ('shop_city', models.CharField(max_length=150)),
                ('shop_area', models.CharField(max_length=500)),
                ('shop_street', models.CharField(max_length=150)),
                ('shop_state', models.CharField(max_length=25)),
                ('slot_duration', models.IntegerField(default=15)),
                ('give_whatsapp_order', models.BooleanField(default=False)),
                ('shop_type', models.IntegerField(validators=[django.core.validators.MaxValueValidator(6)])),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('slot_id', models.UUIDField(default=uuid.UUID('d566001a-63d6-4464-849d-7fa13f344f45'), editable=False, primary_key=True, serialize=False)),
                ('slot_start_time', models.DateTimeField()),
                ('slot_stop_time', models.DateTimeField()),
                ('num_entries_left', models.IntegerField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='main.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='main.Shop'),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='main.Slot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]
