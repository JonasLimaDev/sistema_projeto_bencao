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
#LoginView
urlpatterns = [
    path('login/registrar/', CriarUsusarioView.as_view(), name='criar_usuario'),
    path('login/entrar/', LoginView.as_view(), name='logar_usuario'),

    path('login/sair/', logout_view, name='deslogar'),
    path('perfil/<int:pk>/', PerfilUsuarioView.as_view(), name='dados_tecnico'),

    path('equipe/', EquipeTecnicaView.as_view(), name='equipe_tecnica'),
    # path('adicionar/', adicionar_cadastro,name='adicionar_cadastro'),
    # path('lista/', listar_cadastros,name='listar_cadastros'),
]
