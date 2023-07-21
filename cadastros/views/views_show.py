# Create your views here.
from random import randint

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from ..services import *
from ..filters import *


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
        cadastros = Cadastro.objects.select_related().all()
        argumento = None
        lista_cadastro = []
        context['bairro_busca'] = ""
        context['ruc'] = ""
        context['cras'] = ""
        context['busca'] = ""
        if 'filter' in self.kwargs:
            argumento = self.kwargs['filter']
            if ";" in argumento:
                filters_args = split_filter(argumento)
                if "bairro" in filters_args and "cras" in filters_args and "ruc" in filters_args:
                    lista_cadastro = cadastros.filter(endereco__bairro__nome=filters_args['bairro'],
                                                      abrangencia=filters_args['cras'], endereco__ruc=filters_args['ruc'])
                    context['bairro_busca'] = filters_args['bairro']
                    context['ruc'] = filters_args['ruc']
                    context['cras'] = filters_args['cras']
                elif "bairro" in filters_args and "cras" in filters_args:
                        lista_cadastro = cadastros.filter(endereco__bairro__nome=filters_args['bairro'],
                                                          abrangencia=filters_args['cras'])
                        context['bairro_busca']  = filters_args['bairro']
                        context['cras'] = filters_args['cras']
                elif "bairro" in filters_args and "ruc" in filters_args:
                    lista_cadastro = cadastros.filter(endereco__bairro__nome=filters_args['bairro'],
                                                      endereco__ruc=filters_args['ruc'])
                    context['bairro_busca']  = filters_args['bairro']
                    context['ruc'] = filters_args['ruc']

                elif "cras" in filters_args and "ruc" in filters_args:
                    lista_cadastro = cadastros.filter(abrangencia=filters_args['cras'],
                                                      endereco__ruc=filters_args['ruc'])
                    context['ruc'] = filters_args['ruc']
                    context['cras'] = filters_args['cras']

                elif "bairro" in filters_args:
                    lista_cadastro = cadastros.filter(endereco__bairro__nome=filters_args['bairro'])
                    context['bairro_busca']  = filters_args['bairro']

                elif "cras" in filters_args:
                    lista_cadastro = cadastros.filter(abrangencia=filters_args['cras'])
                    context['cras'] = filters_args['cras']

                elif "ruc" in filters_args:
                    lista_cadastro = cadastros.filter(endereco__ruc=filters_args['ruc'])
                    context['ruc'] = filters_args['ruc']
            else:
                argumento = argumento.split(':')
                
                if "name" in argumento:
                    lista_cadastro = buscar_cadastro_nome(argumento[1])
                    context['busca'] = argumento[1]
                elif "cpf" in argumento:
                    lista_cadastro = buscar_cadastro_cpf(argumento[1])
                    context['busca'] = argumento[1]
                elif "nis_broken_out" in argumento:
                    lista_cadastro = nis_estourado()
                    context['busca'] = argumento[0]
                
                elif "id" in argumento:
                    # cad  = get_object_or_404(Cadastro, id=argumento[1])
                    # print("Sim")
                    # print(vars(cadastros))
                    
                    cad  =  Cadastro.objects.filter(id=argumento[1])
                    if cad:
                        lista_cadastro.append(cad[0])
                    else:
                        context['busca'] = argumento[1]
                elif "inicial" in argumento:
                    lista_cadastro = cadastros.filter(responsavel_familiar__nome__startswith=argumento[1])

            context['cadastros'] = [CadastroData(cadastro_bd) for cadastro_bd in lista_cadastro]
        else:
            context['cadastros'] = [CadastroData(cadastro_bd) for cadastro_bd in cadastros]

        context['alfabeto'] = lista_alfabeto()
        context['total_cadastros'] = len(context['cadastros'])

        paginator = Paginator(context['cadastros'], 20)
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
        filters = ""
        if busca == "nis_broken_out":
            return redirect('listar_cadastros', "nis_broken_out:"+"")
        if not busca and not bairro and not cras and not ruc:
            return redirect('listar_cadastros')
        if busca:
            if is_cpf(busca):
                busca = busca.replace('.', '').replace('-', '').replace(" ", '')
                return redirect('listar_cadastros', "cpf:" + busca)
            elif len(busca) == 11 and busca.isdigit():
                return redirect('listar_cadastros', "cpf:" + busca)
            elif busca.isdigit():
                return redirect('listar_cadastros', "id:" + request.POST['busca'])
            else:
                return redirect('listar_cadastros', "name:" + request.POST['busca'])
        else:
            if bairro:
                filters += f"bairro:{bairro};"
            if ruc:
                filters += f"ruc:{ruc};"
            if cras:
                filters += f"cras:{cras};"
            return redirect('listar_cadastros', filters)


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


