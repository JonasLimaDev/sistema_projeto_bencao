"""perfil_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *


urls_familia = [
    path('cadastros/editar/referencia/<int:pk>/', EditarReferenciaView.as_view(),name='editar_referencia'),
    path('cadastros/adicionar/membro/<int:pk>/', AdicionarMembroView.as_view(),name='adicionar_membro'),
    path('cadastros/editar/membro/<int:pk>/', EditarMembroView.as_view(),name='editar_membro'),
    path('cadastros/excluir/membro/<int:pk>/', ExcluirMembroView.as_view(),name='excluir_membro'),#ExcluirMembroView
]

urls_cadastro =[
    path('cadastros/adicionar/', AdicionarCadastroView.as_view(), name='adicionar_cadastro'),
    path('cadastros/exibir/dados/<int:pk>/', ExibirFichaCadastroView.as_view(), name='exibir_dados_cadastro'),
    path('cadastros/lista/', ListaCadastroView.as_view(), name='listar_cadastros'),
    path('cadastros/lista/<str:filter>/', ListaCadastroView.as_view(), name='listar_cadastros'),
    path('cadastro/editar/<int:pk>/', EditarCadastroView.as_view(), name='editar_cadastro'),

]


outros = [
    path('', HomePageView.as_view(), name='home'),
    path('cadastros/editar/endereco/<int:pk>/', EditarEnderecoView.as_view(),name='editar_endereco'),
    path('cadastros/editar/habitacao/<int:pk>/', EditarHabitacaoView.as_view(), name='editar_habitacao'),
    path('cadastros/adicionar/habitacao/<int:pk>/', AdicionarHabitacaoView.as_view(), name='adicionar_habitacao'),

    path('cadastros/json/', dados_cadastro_json, name='json'),
    path('cadastros/avançado/upload/dados/', EnviarDados.as_view(), name='upload_dados'),

    path('dados/tabelas/', RenderData.as_view(), name='dados_tabelas'),
]

urlpatterns = urls_familia + urls_cadastro + outros