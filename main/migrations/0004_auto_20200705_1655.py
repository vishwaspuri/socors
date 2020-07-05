# Generated by Django 2.1.8 on 2020-07-05 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200610_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='gpay_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='owners_remark',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='paytm_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='phonepe_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='breakday',
            unique_together={('shop', 'day')},
        ),
    ]
