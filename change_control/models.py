from django.db import models


# Create your models here.
class CampoChange(models.Model):
    class Meta:
        verbose_name = "Campo Modificado"
        verbose_name_plural = "Campos Modificados"

    campo = models.CharField(max_length=60, null=False, blank=False, verbose_name="Campo Alterado")
    novo_valor = models.TextField(verbose_name="Novo Valor")
    antigo_valor = models.TextField(verbose_name="Valor Antigo")
    modificacao = models.ForeignKey("Alteracao", on_delete=models.CASCADE)

    def __str__(self):
        return self.campo


class TabelaDadosChange(models.Model):
    class Meta:
        verbose_name = "Adição de Dados"
        verbose_name_plural = "Adições de Dados"

    tabela = models.CharField(max_length=60, null=False, blank=False, verbose_name="Grupo Adicionado")
    relacao = models.CharField(max_length=60, null=False, blank=False, verbose_name="Relação")
    modificacao = models.ForeignKey("Alteracao", on_delete=models.CASCADE)

    def __str__(self):
        return self.tabela


class Alteracao(models.Model):
    class Meta:
        verbose_name = "Alteração"
        verbose_name_plural = "Alterações"

    TIPOS = (
        ('1', 'Adição'),
        ('2', 'Edição'),
        ('3', 'Exclusão'),
    )
    
    tipo_acao = models.CharField(max_length=1, choices=TIPOS, null=False, blank=False, verbose_name="Tipo da Alteração")
    data_modificacao = models.DateTimeField(auto_now=True, verbose_name="Data de Modificação")
    id_alterado = models.IntegerField(null=False, blank=False, verbose_name="ID Alterado")
    tabela = models.CharField(max_length=60, null=False, blank=False, verbose_name="Tabela Alterada")
    indicador_alterado = models.CharField(max_length=200, null=True, blank=True,
                                          verbose_name="Indicador do Dado Alterado")
    responsavel = models.ForeignKey("tecnicos.Tecnico", on_delete=models.CASCADE,
                                    verbose_name="Responsável Pela Alteração")

    def __str__(self):
        return self.tipo_acao