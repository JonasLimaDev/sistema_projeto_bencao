# Generated by Django 4.1.3 on 2023-02-24 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tecnicos', '0001_initial'),
        ('cadastros', '0009_cadastro_data_alteracao'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastro',
            name='responsavel_cadastro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tecnicos.tecnico'),
        ),
    ]
