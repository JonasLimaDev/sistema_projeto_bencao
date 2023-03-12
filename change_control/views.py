from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from .classes_change_control import DataAcoes
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from .classes_change_control import DataAcoes
from .models import *
# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListaModificacoesView(TemplateView):
    template_name = 'tabelas_modificacoes.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        argumento = None
        modificacoes = Acao.objects.select_related().all()
        # l = [DataAcoes(modificacao_bd) for modificacao_bd in modificacoes]
        # print(l)
        # # cadastros = Cadastro.objects.all()
        # if 'filter' in self.kwargs:
        #     argumento = self.kwargs['filter']
        #     if "name" in argumento:
        #         argumento = argumento.split(':')
        #     elif "id" in argumento:
        #         argumento = argumento.split(':')
        #     elif "bairro" in argumento:
        #         argumento = argumento.split(':')
        #     elif "inicial" in argumento:
        #         argumento = argumento.split(':')
        #     elif "cpf" in argumento:
        #         argumento = argumento.split(':')
        #     elif "cras" in argumento:
        #         argumento = argumento.split(':')
        #     elif "ruc" in argumento:
        #         argumento = argumento.split(':')
        #
        # if argumento:
        #     lista_cadastro = []
        #     if argumento[0] == 'name':
        #         lista_cadastro = buscar_cadastro_nome(argumento[1])
        #     elif argumento[0] == 'cpf':
        #         lista_cadastro = buscar_cadastro_cpf(argumento[1])
        #     elif argumento[0] == 'bairro':
        #         context["busca_bairro"] = argumento[1]
        #         lista_cadastro = buscar_cadastro_bairro(argumento[1])
        #     elif argumento[0] == 'ruc':
        #         context["busca_ruc"] = argumento[1]
        #         lista_cadastro = buscar_cadastro_ruc(argumento[1])
        #     elif argumento[0] == 'cras':
        #         context["busca_cras"] = argumento[1]
        #         lista_cadastro = cadastros.filter(abrangencia=argumento[1])
        #     elif argumento[0] == 'inicial':
        #         lista_cadastro = cadastros.filter(responsavel_familiar__nome__startswith=argumento[1])
        #     elif argumento[0] == 'id':
        #         lista_cadastro.append(get_object_or_404(Cadastro, id=argumento[1]))
        #
        #     context['cadastros'] = [CadastroData(cadastro_bd) for cadastro_bd in lista_cadastro]
        # else:
        context['dados_modificacoes'] = [DataAcoes(modificacao_bd) for modificacao_bd in modificacoes]
        context['dados_modificacoes'] = context['dados_modificacoes']
        return context

    def post(self, request, *args, **kwargs):
        busca = request.POST['busca']

        bairro = request.POST['bairro']
        cras = request.POST['cras'] if request.POST['cras'] != "-------" else None
        ruc = request.POST['ruc'] if request.POST['ruc'] != "-------" else None
        if busca:
            if is_cpf(busca):
                busca = busca.replace('.', '').replace('-', '').replace(" ", '')
                return redirect('listar_cadastros', "cpf:" + busca)
            if len(busca) == 11 and busca.isdigit():
                return redirect('listar_cadastros', "cpf:" + busca)
            elif busca.isdigit():
                return redirect('listar_cadastros', "id:" + request.POST['busca'])
            else:
                return redirect('listar_cadastros', "name:" + request.POST['busca'])
        elif bairro:
            return redirect('listar_cadastros', "bairro:" + request.POST['bairro'])
        elif ruc:
            return redirect('listar_cadastros', "ruc:" + request.POST['ruc'])
        elif cras:
            return redirect('listar_cadastros', "cras:" + request.POST['cras'])
        else:
            return redirect('listar_cadastros')
