# Generated by Django 5.0.7 on 2024-07-22 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_profile_has_outstanding_debt'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentschedule',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('in_process', 'En proceso'), ('paid', 'Pagado'), ('overdue', 'Atrasado')], default='pending', max_length=20),
        ),
    ]
