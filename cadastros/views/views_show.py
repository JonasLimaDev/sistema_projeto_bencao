import json
import os
# Create your views here.
from random import randint

from django.http import JsonResponse
from django.views import View
from ..validations import is_cpf_valid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tecnicos.models import Tecnico
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from time import sleep
from ..entidades.dados import *
from ..forms import *
from ..models import *
from ..services import *
from ..filters import *
from pprint import pprint
from change_control.services import create_change_campos
from change_control.classes_change_control import ChangeCampoData


def gerar_valores(mes_dict):
    for mes in mes_dict:
        mes_dict[mes] = randint(20, 249)
    return mes_dict


def lista_alfabeto():
    lista_alfabeto = {}
    for valor in range(ord('A'), ord('Z') + 1):
        lista_alfabeto[chr(valor)] = f"inicial:{chr(valor)}"
    return lista_alfabeto


class HomePageView(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
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


@method_decorator(login_required, name='dispatch')
class RenderData(TemplateView):
    template_name = 'cadastros/geral/tabelas_dados.html'

    def get(self, request, *args, **kwargs):
        dados_bairros = total_cadastro_bairro()
        dados_rucs = total_cadastro_ruc()
        dados_cras = total_cadastro_cras()
        return render(request, self.template_name,
                      {'dados_bairros': dados_bairros, 'dados_rucs': dados_rucs, 'dados_cras': dados_cras})


@method_decorator(login_required, name='dispatch')
class ListaCadastroView(TemplateView):
    template_name = 'cadastros/geral/lista_cadastros.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        bairros = Bairro.objects.select_related().all()
        argumento = None
        cadastros = Cadastro.objects.select_related().all()
        # cadastros = Cadastro.objects.all()
        if 'filter' in self.kwargs:
            argumento = self.kwargs['filter']
            if "name" in argumento:
                argumento = argumento.split(':')
            elif "id" in argumento:
                argumento = argumento.split(':')
            elif "bairro" in argumento:
                argumento = argumento.split(':')
            elif "inicial" in argumento:
                argumento = argumento.split(':')
            elif "cpf" in argumento:
                argumento = argumento.split(':')
            elif "cras" in argumento:
                argumento = argumento.split(':')
            elif "ruc" in argumento:
                argumento = argumento.split(':')

        if argumento:
            lista_cadastro = []
            if argumento[0] == 'name':
                lista_cadastro = buscar_cadastro_nome(argumento[1])
            elif argumento[0] == 'cpf':
                lista_cadastro = buscar_cadastro_cpf(argumento[1])
            elif argumento[0] == 'bairro':
                context["busca_bairro"] = argumento[1]
                lista_cadastro = buscar_cadastro_bairro(argumento[1])
            elif argumento[0] == 'ruc':
                context["busca_ruc"] = argumento[1]
                lista_cadastro = buscar_cadastro_ruc(argumento[1])
            elif argumento[0] == 'cras':
                context["busca_cras"] = argumento[1]
                lista_cadastro = cadastros.filter(abrangencia=argumento[1])
            elif argumento[0] == 'inicial':
                lista_cadastro = cadastros.filter(responsavel_familiar__nome__startswith=argumento[1])
            elif argumento[0] == 'id':
                lista_cadastro.append(get_object_or_404(Cadastro, id=argumento[1]))
            # print(argumento)
            context['cadastros'] = [CadastroData(cadastro_bd) for cadastro_bd in lista_cadastro]
        else:
            context['cadastros'] = [CadastroData(cadastro_bd) for cadastro_bd in cadastros]
        context['alfabeto'] = lista_alfabeto()
        context['total_cadastros'] = len(context['cadastros'])

        paginator = Paginator(context['cadastros'], 20)  # Show 25 contacts per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['page_range'] = paginator.get_elided_page_range(page_obj.number)
        # print(context['page_range'])
        context['lista_bairros'] = bairros
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


@method_decorator(login_required, name='dispatch')
class ExibirFichaCadastroView(TemplateView):
    # form_habitacao = FormHabitacao
    template_name = "cadastros/geral/dados_cadastro.html"
    context = {'titulo_pagina': "Dados Cadastro"}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['cadastro'] = CadastroData(cadastro)
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class ExibirDadosCadastroView(TemplateView):
    template_name = "cadastros/geral/dados_cadastro.html"
    context = {'titulo_pagina': "Dados Cadastro"}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['cadastro'] = CadastroData(cadastro)

        return render(request, self.template_name, self.context)


