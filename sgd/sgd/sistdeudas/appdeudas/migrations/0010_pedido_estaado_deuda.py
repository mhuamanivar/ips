# Generated by Django 5.0.6 on 2024-06-11 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdeudas', '0009_remove_cliente_codigo_remove_trabajador_codigo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='estaado_deuda',
            field=models.CharField(choices=[('V', 'Vigente'), ('C', 'Cerrado')], default='A', max_length=1),
        ),
    ]