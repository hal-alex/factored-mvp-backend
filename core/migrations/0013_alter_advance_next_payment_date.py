# Generated by Django 4.1.5 on 2023-01-16 18:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_advance_next_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advance',
            name='next_payment_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]