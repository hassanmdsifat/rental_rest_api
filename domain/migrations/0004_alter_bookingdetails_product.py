# Generated by Django 3.2 on 2021-12-13 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0003_auto_20211213_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_details', to='domain.product'),
        ),
    ]
