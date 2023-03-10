from django.db import models

# Create your models here.
class Alteracao(models.Model):
    class Meta:
        verbose_name = "Alteração"
        verbose_name_plural = "Alterações"
            
    campo = models.CharField(max_length=60, null=False, blank=False, verbose_name="Campo Alterado")
    novo_valor = models.TextField(verbose_name="Novo Valor")
    novo_antigo_valor = models.TextField(verbose_name="Valor Antigo")
    data_modificacao = models.DateTimeField(auto_now=True,verbose_name="Data de Modificação")
    responsavel = models.ForeignKey("tecnicos.Tecnico",on_delete=models.CASCADE, verbose_name="Responsável Pela Alteração")
    
    def __str__(self):
        return self.nome_equipamento