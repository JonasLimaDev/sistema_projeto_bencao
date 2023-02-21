from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

class Orgaos(models.Model):
    nome_orgao = models.CharField(max_length=200, null=False, blank=False)
    sigla = models.CharField(max_length=15, null=False, blank=False, default="")

    class Meta:
        verbose_name = "Órgão"
        verbose_name_plural = "Órgãos"
    def __str__(self):
        return self.sigla



class Tecnico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name = "Usuário")
    orgao = models.ForeignKey(Orgaos,on_delete=models.PROTECT, verbose_name="Órgão")
    cargo = models.CharField(max_length=150, null=False, blank=False)
    # email = models.CharField(max_length=150, null=False, blank=False)
    contato = models.CharField(max_length=20, null=True, blank=True)
    cadastro_pendente = models.BooleanField(default=True)
    data_registro = models.DateField(null=False,blank=False,default=datetime.now)

    def __str__(self):
        return self.usuario.get_full_name()
    
    
