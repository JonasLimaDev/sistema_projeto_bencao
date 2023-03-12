from django.urls import path
from .views import *

urlpatterns = [
    path('tabela_alteracoes/', ListaModificacoesView.as_view(), name='lista_alteracoes'),
]