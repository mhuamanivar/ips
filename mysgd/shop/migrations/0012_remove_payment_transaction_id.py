# Generated by Django 5.0.7 on 2024-07-15 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_orderitem_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='transaction_id',
        ),
    ]
