# Generated by Django 5.0.7 on 2024-07-22 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_remove_paymentschedule_schedule_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('in_preparation', 'En preparación'), ('prepared', 'Preparado'), ('delivered', 'Entregado'), ('delivered_in_debt', 'Entregado en deuda'), ('completed', 'Finalizado'), ('cancelled', 'Anulado')], default='pending', max_length=20),
        ),
    ]