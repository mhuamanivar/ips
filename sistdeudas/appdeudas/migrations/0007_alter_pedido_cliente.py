# Generated by Django 5.0.6 on 2024-06-10 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdeudas', '0006_cronograma_usuariopersonalizado_trabajador_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appdeudas.cliente'),
        ),
    ]
