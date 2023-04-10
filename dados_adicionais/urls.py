from django.urls import path
from .views import *

urlpatterns = [
    path('adicionar/identificacao/<int:pk>/', AddExtrasView.as_view(), name='adicionar_extras'),
    path('editar/identificacao/<int:pk>/', EditExtrasView.as_view(), name='editar_extras'),

    path('adicionar/informacoes/bancarias/<int:pk>/', AddDadosBancariosView.as_view(), name='adicionar_banco'),
    path('editar/informacoes/bancarias/<int:pk>/', EditDadosBancariosView.as_view(), name='editar_banco'),


    path('adicionar/informacoes/educacionais/<int:pk>/<int:sk>/', AddDadosEducacaoView.as_view(), name='adicionar_educacao'),
    path('editar/informacoes/educacionais/<int:sk>/<int:pk>/', EditDadosEducacaoView.as_view(), name='editar_educacao'),
    path('adicionar/informacoes/saude/<int:pk>/<int:sk>/', AddDadosSaudeView.as_view(), name='adicionar_saude'),
    path('editar/informacoes/saude/<int:sk>/<int:pk>/', EditDadosSaudeView.as_view(), name='editar_saude'),
]