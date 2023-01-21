# Generated by Django 4.1.5 on 2023-01-17 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_advance_loan_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advance',
            name='reason',
            field=models.CharField(choices=[('Debt', 'Consolidating debt'), ('Improvement', 'Home improvement/repair'), ('Car', 'Car'), ('Occasion', 'Special occasion/event'), ('Other', 'Other')], default='Other', max_length=100),
        ),
        migrations.AlterField(
            model_name='advance',
            name='status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Pending approval', 'Pending approval'), ('Active', 'Active'), ('In arrears', 'In arrears'), ('Repaid', 'Repaid')], default='Incomplete', max_length=16),
        ),
    ]