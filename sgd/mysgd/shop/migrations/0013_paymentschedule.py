# Generated by Django 5.0.7 on 2024-07-21 21:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_payment_transaction_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.PositiveIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_schedules', to='shop.order')),
            ],
        ),
    ]