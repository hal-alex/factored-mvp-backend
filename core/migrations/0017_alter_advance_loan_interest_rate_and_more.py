# Generated by Django 4.1.5 on 2023-01-16 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_advance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advance',
            name='loan_interest_rate',
            field=models.DecimalField(choices=[(0.2399, '23.99%'), (0.2199, '21.99%'), (0.1999, '19.99%'), (0.1799, '17.99%'), (0.1599, '15.99%'), (0.1399, '13.99%'), (0.1299, '12.99%')], decimal_places=5, default=0.2399, max_digits=8),
        ),
        migrations.AlterField(
            model_name='advance',
            name='loan_term',
            field=models.PositiveIntegerField(choices=[(3, '3 months'), (6, '6 months'), (12, '12 months'), (24, '24 months'), (36, '36 months'), (48, '48 months'), (60, '60 months')], default=3, max_length=2),
        ),
    ]
