# Generated by Django 4.1.7 on 2023-02-22 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_delete_dadosaude_pessoa_dados_saude_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cadastro',
            options={'ordering': ('responsavel_familiar__nome',)},
        ),
        migrations.AlterModelOptions(
            name='pessoa',
            options={'ordering': ('nome',), 'verbose_name': 'Pessoa', 'verbose_name_plural': 'Pessoas'},
        ),
        migrations.AddField(
            model_name='referencia',
            name='entrevistador',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Entrevistador'),
        ),
    ]
