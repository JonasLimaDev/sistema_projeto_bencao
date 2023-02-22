from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404
#
from .. models import Cadastro, Endereco,Habitacao, Referencia, Identificacao, Pessoa
from ..forms import FormEndereco, FormHabitacao
from ..services import editar_endereco, inserir_bairros


class HomePageView(TemplateView):
    template_name = 'base.html'

    def get(self,request,*args, **kwargs):
        dados = {}
        # inserir_bairros()
        # orgs = ["CRAS I","CRAS II","CRAS III","CREAS","SEMAPS - SEDE","Projeto"]
        # for org in orgs:
        #     mes = {'Jan':0, "Fev":0,'Mar':0, "Abr":0,
        # 'Mai':0,"Jun":0,'Jul':0, "Ago":0,
        # 'Set':0, "Out":0,'Nov':0, "Dez":0,}
        #     lista = gerar_valores(mes)
        #     dados[org]=lista
        return render(request, self.template_name, {'dados': dados})








def handler500(request):
    return render(request,'500.html')


def handler404(request, exception):
    return render(request, '404.html')
