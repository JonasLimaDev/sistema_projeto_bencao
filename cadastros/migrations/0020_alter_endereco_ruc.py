# Generated by Django 4.1.3 on 2023-05-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0019_alter_referencia_cor_raca_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='ruc',
            field=models.CharField(blank=True, choices=[('1', 'Nenhum'), ('2', 'Água Azul'), ('3', 'Jatobá'), ('4', 'São Joaquim'), ('5', 'Casa Nova'), ('6', 'Laranjeiras'), ('7', 'Tavaquara')], default='1', max_length=1, null=True, verbose_name='RUC'),
        ),
    ]
