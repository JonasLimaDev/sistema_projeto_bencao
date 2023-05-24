# Generated by Django 4.1.3 on 2023-05-24 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0017_referencia_dados_bancarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacao',
            name='pavimentacao',
            field=models.CharField(choices=[('1', 'Asfalto'), ('2', 'Bloqueteamento'), ('3', 'Não Possui'), ('4', 'Não Informado')], max_length=1, verbose_name='Pavimentação da Rua'),
        ),
        migrations.AlterField(
            model_name='habitacao',
            name='possui_abastecimento',
            field=models.CharField(choices=[('1', 'Rede Geral de Distribuição'), ('2', 'Poço'), ('3', 'Fonte, Nascente ou Mina'), ('4', ' Carro-Pipa'), ('5', 'Água da Chuva Armazenada'), ('6', ' Rios, Açudes, Córregos, Lagos e Igarapés'), ('7', 'Outra'), ('8', 'Não Informado')], max_length=1, verbose_name='Abastecimento de Água'),
        ),
        migrations.AlterField(
            model_name='habitacao',
            name='possui_coleta',
            field=models.CharField(choices=[('1', 'Coletado no Domicílio Por Serviço de Limpeza'), ('2', 'Depositado em Caçamba de Serviço de Limpeza '), ('3', 'Queimado na Propriedade'), ('4', 'Enterrado na Propriedade'), ('5', 'Jogado em Terreno Baldio, Encosta ou Área Pública'), ('6', 'Outro Destino'), ('7', 'Não Informado')], max_length=1, verbose_name='Coleta de Lixo'),
        ),
        migrations.AlterField(
            model_name='habitacao',
            name='possui_rede_esgoto',
            field=models.CharField(choices=[('1', 'Rede Geral ou Pluvial'), ('2', 'Fossa Rudimentar ou Buraco'), ('3', 'Vala'), ('4', 'Não Possui'), ('5', 'Não Informado')], max_length=1, verbose_name='Possui Rede de Esgoto'),
        ),
        migrations.AlterField(
            model_name='habitacao',
            name='rede_eletrica',
            field=models.CharField(choices=[('1', 'Com Medidor Próprio'), ('2', 'Sem Padrão'), ('3', 'Não Possui'), ('4', 'Não Informado')], max_length=1, verbose_name='Possui Energia Elétrica'),
        ),
        migrations.AlterField(
            model_name='habitacao',
            name='situacao_moradia',
            field=models.CharField(choices=[('1', 'Alugada'), ('2', 'Própria'), ('3', 'Cedida'), ('4', 'Invasão'), ('5', 'Sem Moradia Fixa'), ('6', 'Não Informado')], max_length=1, verbose_name='Situação da Moradia'),
        ),
        migrations.AlterField(
            model_name='habitacao',
            name='tipo_construcao',
            field=models.CharField(choices=[('1', 'Alvenaria'), ('2', 'Barro'), ('3', 'Madeira'), ('4', 'Outro'), ('5', 'Não Se Aplica'), ('6', 'Não Informado')], max_length=1, verbose_name='Tipo de Construção'),
        ),
    ]