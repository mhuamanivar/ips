# Generated by Django 5.0.7 on 2024-07-21 23:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_paymentschedule_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentschedule',
            old_name='is_paid',
            new_name='paid',
        ),
        migrations.AlterUniqueTogether(
            name='paymentschedule',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='paymentschedule',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='shop.order'),
        ),
    ]
