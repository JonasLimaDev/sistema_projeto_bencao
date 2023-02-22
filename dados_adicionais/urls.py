from django.urls import path
from .views import *

urlpatterns = [
    path('adicionar/identificacao/<int:pk>/', AdicinarExtrasView.as_view(), name='adicionar_extras'),
    path('editar/identificacao/<int:pk>/', EditarExtrasView.as_view(), name='editar_extras'),

    path('adicionar/dados/educacao/<int:pk>/<int:sk>/', AddDadosEducacaoView.as_view(), name='adicionar_educacao'),
    path('editar/dados/educacao/<int:sk>/<int:pk>/', EditDadosEducacaoView.as_view(), name='editar_educacao'),
    path('adicionar/dados/saude/<int:pk>/<int:sk>/', AddDadosSaudeView.as_view(), name='adicionar_saude'),
    path('editar/dados/saude/<int:sk>/<int:pk>/', EditDadosSaudeView.as_view(), name='editar_saude'),
]