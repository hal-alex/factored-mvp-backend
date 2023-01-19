# Generated by Django 4.1.5 on 2023-01-19 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_advance_loan_interest_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advance',
            name='loan_interest_rate',
            field=models.DecimalField(choices=[('0.2399', '0.2399'), ('0.2199', '0.2199'), ('0.1999', '0.1999'), ('0.1799', '0.1799'), ('0.1599', '0.1599'), ('0.1399', '0.1399'), ('0.1299', '0.1299')], decimal_places=4, default=0.2399, max_digits=8),
        ),
    ]
