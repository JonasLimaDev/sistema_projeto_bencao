from django.urls import path

from .views.views_edit import EditDadosSaudeView, EditExtrasView, \
    EditDadosEducacaoView, EditDadosBancariosView

from .views.views_add import AddExtrasView, AddDadosEducacaoView, \
    AddDadosSaudeView, AddDadosBancariosView


urls_add = [
    path('adicionar/identificacao/<int:pk>/', AddExtrasView.as_view(), name='adicionar_extras'),
    path('adicionar/informacoes/bancarias/<int:pk>/', AddDadosBancariosView.as_view(), name='adicionar_banco'),
    path('adicionar/informacoes/saude/<int:pk>/<int:sk>/', AddDadosSaudeView.as_view(), name='adicionar_saude'),
    path('adicionar/informacoes/educacionais/<int:pk>/<int:sk>/', AddDadosEducacaoView.as_view(),
         name='adicionar_educacao'),
]

urls_edit = [
    path('editar/identificacao/<int:pk>/', EditExtrasView.as_view(), name='editar_extras'),
    path('editar/informacoes/bancarias/<int:pk>/', EditDadosBancariosView.as_view(), name='editar_banco'),
    path('editar/informacoes/educacionais/<int:sk>/<int:pk>/', EditDadosEducacaoView.as_view(),
         name='editar_educacao'),
    path('editar/informacoes/saude/<int:sk>/<int:pk>/', EditDadosSaudeView.as_view(), name='editar_saude'),
]

urlpatterns = urls_add + urls_edit