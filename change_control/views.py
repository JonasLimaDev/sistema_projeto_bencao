from django.views.generic import TemplateView
from .classes_change_control import DataAlteracoes
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListaModificacoesView(TemplateView):
    template_name = 'change_control/tabelas_modificacoes.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        argumento = None
        modificacoes = Alteracao.objects.select_related().all()
        context['dados_modificacoes'] = [DataAlteracoes(modificacao_bd) for modificacao_bd in modificacoes]
        return context