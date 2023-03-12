# Generated by Django 4.1.7 on 2023-03-12 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tecnicos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_acao', models.CharField(choices=[('1', 'Adição'), ('2', 'Edição'), ('3', 'Exclusão')], max_length=1, verbose_name='Campo Alterado')),
                ('data_modificacao', models.DateTimeField(auto_now=True, verbose_name='Data de Modificação')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tecnicos.tecnico', verbose_name='Responsável Pela Alteração')),
            ],
            options={
                'verbose_name': 'Alteração',
                'verbose_name_plural': 'Alterações',
            },
        ),
        migrations.CreateModel(
            name='TabelaDadosChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabela', models.CharField(max_length=60, verbose_name='Grupo Adicionado')),
                ('relacao', models.CharField(max_length=60, verbose_name='Relação')),
                ('modificacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='change_control.acao')),
            ],
            options={
                'verbose_name': 'Adição de Dados',
                'verbose_name_plural': 'Adições de Dados',
            },
        ),
        migrations.CreateModel(
            name='CampoChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo', models.CharField(max_length=60, verbose_name='Campo Alterado')),
                ('novo_valor', models.TextField(verbose_name='Novo Valor')),
                ('antigo_valor', models.TextField(verbose_name='Valor Antigo')),
                ('modificacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='change_control.acao')),
            ],
            options={
                'verbose_name': 'Campo Modificado',
                'verbose_name_plural': 'Campos Modificados',
            },
        ),
    ]
