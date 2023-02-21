from django.contrib import admin
from .models import *


# Register your models here.


class AdminOrgao(admin.ModelAdmin):
    list_display = ('id', 'sigla', 'nome_orgao')
    list_display_links = ('id', 'sigla',)


admin.site.register(Orgaos, AdminOrgao)


class AdminTecnico(admin.ModelAdmin):
    list_display = ('id', 'usuario', '__str__', 'orgao', 'cargo', 'email_usuario')
    list_filter = ('orgao', 'cargo',)
    list_display_links = ('usuario',)

    # search_fields = ['nome']
    def email_usuario(self, obj):
        return obj.usuario.email


admin.site.register(Tecnico, AdminTecnico)
