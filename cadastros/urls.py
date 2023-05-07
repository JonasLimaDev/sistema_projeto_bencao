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
from .views.views_create import AddCadastroView, AddHabitacaoView, AddMembroView
from .views.views_delete import DeleteMembroView
from .views.views_printer import PrinterTableView, PrinterFichaView
from .views.views_data_and_handler import UploadDados, get_dados_json
from .views.views_edit import EditCadastroView, EditEnderecoView, EditReferenciaView, \
    EditHabitacaoView, EditMembroView

from .views.views_show import *

urls_add = [
    path('cadastros/adicionar/membro/<int:pk>/', AddMembroView.as_view(),name='adicionar_membro'),
    path('cadastros/adicionar/habitacao/<int:pk>/', AddHabitacaoView.as_view(), name='adicionar_habitacao'),
    path('cadastros/adicionar/', AddCadastroView.as_view(), name='adicionar_cadastro'),
]

urls_edit = [
    path('cadastros/editar/referencia/<int:pk>/', EditReferenciaView.as_view(), name='editar_referencia'),
    path('cadastros/editar/membro/<int:pk>/', EditMembroView.as_view(), name='editar_membro'),
    path('cadastro/editar/<int:pk>/', EditCadastroView.as_view(), name='editar_cadastro'),

]

urls_delete = [
    path('cadastros/excluir/membro/<int:pk>/', DeleteMembroView.as_view(),name='excluir_membro'),
]

urls_show = [

    path('', HomePageView.as_view(), name='home'),
    path('dados/tabelas/', RenderData.as_view(), name='dados_tabelas'),
    path('cadastros/exibir/informacoes/<int:pk>/', ExibirFichaCadastroView.as_view(), name='exibir_dados_cadastro'),
    path('cadastros/lista/', ListaCadastroView.as_view(), name='listar_cadastros'),
    path('cadastros/lista/<str:filter>/', ListaCadastroView.as_view(), name='listar_cadastros'),
    path('cadastros/editar/endereco/<int:pk>/', EditEnderecoView.as_view(), name='editar_endereco'),
    path('cadastros/editar/habitacao/<int:pk>/', EditHabitacaoView.as_view(), name='editar_habitacao'),


]

urls_printer = [
    path('printer/dados/tabela/total/<str:filter>/', PrinterTableView.as_view(), name='dados_pdf'),
    path('printer/dados/cadastro/<int:pk>/', PrinterFichaView.as_view(), name='ficha_pdf'),# PrinterFichaView
]

urls_data = [
    path('dados/uploads/', UploadDados.as_view(), name='upload_dados'),
    path('dados/json/', get_dados_json, name='json'),
]

outros = [

]

urlpatterns = urls_add +urls_edit+ urls_show + urls_delete + urls_data + urls_printer