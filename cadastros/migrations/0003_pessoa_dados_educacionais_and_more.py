# Generated by Django 4.1.3 on 2023-02-16 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0002_alter_membros_parentesco_alter_pessoa_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='dados_educacionais',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.dadoseducacao'),
        ),
        migrations.AlterField(
            model_name='dadoseducacao',
            name='nivel_curso',
            field=models.CharField(blank=True, choices=[('1', 'Alfabetização'), ('2', 'Ensino Infantil'), ('3', 'Ensino Fundamental'), ('4', 'Ensino Médio'), ('5', 'Ensino Técnico'), ('6', 'Ensino Superior'), ('7', 'Pós Graduação'), ('8', 'Outro'), ('9', 'Nenhum')], max_length=1, null=True, verbose_name='Está Cursando?'),
        ),
    ]
