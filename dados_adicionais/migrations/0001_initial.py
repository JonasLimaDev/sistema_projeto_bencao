# Generated by Django 4.1.7 on 2023-02-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Educacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estuda', models.CharField(choices=[('1', 'Sim'), ('2', 'Não')], max_length=1, verbose_name='Está Estudando?')),
                ('nivel_curso', models.CharField(blank=True, choices=[('1', 'Alfabetização'), ('2', 'Ensino Infantil'), ('3', 'Ensino Fundamental'), ('4', 'Ensino Médio'), ('5', 'Ensino Técnico'), ('6', 'Ensino Superior'), ('7', 'Pós Graduação'), ('8', 'Outro'), ('9', 'Nenhum')], max_length=1, null=True, verbose_name='Está Cursando?')),
                ('local', models.CharField(blank=True, max_length=60, null=True, verbose_name='Local Onde Estuda')),
            ],
            options={
                'verbose_name': 'Dado de Educação',
                'verbose_name_plural': 'Dados Educacionais',
            },
        ),
        migrations.CreateModel(
            name='Identificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rg', models.CharField(max_length=16, verbose_name='Nº RG')),
                ('orgao_emissor', models.CharField(max_length=25, verbose_name='Órgão Emissor (RG)')),
                ('data_emissao', models.DateField(verbose_name='Data de Emissão (RG)')),
                ('titulo_eleitor', models.CharField(max_length=25, verbose_name='Nº Titulo de Eleitor')),
                ('zona', models.CharField(max_length=5, verbose_name='Zona Eleitoral')),
                ('secao', models.CharField(max_length=5, verbose_name='Seção Eleitoral')),
                ('natural_cidade', models.CharField(max_length=50, verbose_name='Cidade de Naturalidade')),
                ('natural_estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado Naturalidade')),
            ],
        ),
        migrations.CreateModel(
            name='Saude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deficiencia', models.CharField(choices=[('1', 'Sim'), ('2', 'Não')], max_length=1, verbose_name='Possui Deficiência?')),
                ('tipo_deficiencia', models.CharField(blank=True, choices=[('1', 'Física'), ('2', 'Auditiva'), ('3', 'Visual'), ('4', 'Mental/Intelectual'), ('5', 'Múltipla')], max_length=1, null=True, verbose_name='Especifique o Tipo de Deficiência')),
                ('gravidez', models.CharField(blank=True, choices=[('1', 'Gravida'), ('2', 'Não Grávida'), ('3', 'Não Se Aplica')], max_length=1, null=True, verbose_name='Gravidez')),
            ],
            options={
                'verbose_name': 'Dado de Saúde',
                'verbose_name_plural': 'Dados Saúde',
            },
        ),
    ]
