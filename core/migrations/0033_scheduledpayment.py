# Generated by Django 4.1.5 on 2023-01-21 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_passwordresettoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledPayment',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='ABCDEFGHJKLMNPQRSTUVWXYZ23456789', editable=False, length=8, max_length=8, prefix='', primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('Not due yet', 'Not due yet'), ('Due', 'Due'), ('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Not due yet', max_length=25)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('due_date', models.DateField()),
                ('advance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.advance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
