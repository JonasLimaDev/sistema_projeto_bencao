import json
import os
# Create your views here.
from random import randint

from django.http import JsonResponse
from .validations import is_cpf_valid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tecnicos.models import Tecnico
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from .entidades.dados import *
from .forms import *
from .models import *
from .services import *
from pprint import pprint

def gerar_valores(mes_dict):
    for mes in mes_dict:
        mes_dict[mes] = randint(20, 249)
    return mes_dict

def lista_alfabeto():
    lista_alfabeto = {}
    for valor in range(ord('A'), ord('Z')+1):
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


class RenderData(TemplateView):
    template_name = 'tabelas_dados.html'

    def get(self, request, *args, **kwargs):
        dados_bairros = total_cadastro_bairro()
        dados_rucs = total_cadastro_ruc()
        dados_cras = total_cadastro_cras()
        # inserir_bairros()
        # orgs = ["CRAS I","CRAS II","CRAS III","CREAS","SEMAPS - SEDE","Projeto"]
        # for org in orgs:
        #     mes = {'Jan':0, "Fev":0,'Mar':0, "Abr":0,
        # 'Mai':0,"Jun":0,'Jul':0, "Ago":0,
        # 'Set':0, "Out":0,'Nov':0, "Dez":0,}
        #     lista = gerar_valores(mes)
        #     dados[org]=lista
        return render(request, self.template_name, {'dados_bairros': dados_bairros,'dados_rucs':dados_rucs,'dados_cras':dados_cras})



@method_decorator(login_required, name='dispatch')
class ListaCadastroView(TemplateView):
    template_name = 'cadastros/lista_cadastros.html'

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
            elif argumento[0] =='bairro':
                context["busca_bairro"] = argumento[1]
                lista_cadastro = buscar_cadastro_bairro(argumento[1])
            elif argumento[0] =='ruc':
                context["busca_ruc"] = argumento[1]
                lista_cadastro = buscar_cadastro_ruc(argumento[1])
            elif argumento[0] =='cras':
                context["busca_cras"] = argumento[1]
                lista_cadastro = cadastros.filter(abrangencia=argumento[1])
            elif argumento[0] =='inicial':
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
        ruc = request.POST['ruc'] if  request.POST['ruc'] != "-------" else None
        if busca:
            if is_cpf(busca):
                busca = busca.replace('.','').replace('-','').replace(" ",'')
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
class AdicionarCadastroView(TemplateView):
    form_referencia = FormReferencia
    form_endereco = FormEndereco
    form_habitacao = FormHabitacao
    form_cadastro = FormCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Adicionar Cadastro", 'link': '/cadastros/lista/'}

    def get(self, request, *args, **kwargs):
        forms_generic = {"Informações da Referência Familiar": self.form_referencia(),
                         "Informações de Endereço": self.form_endereco(),
                         "Informações da Moradia": self.form_habitacao(),
                         "Informações do Cadastramento": self.form_cadastro(),
                         }
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form1 = self.form_referencia(request.POST)
        form2 = self.form_endereco(request.POST)
        form3 = self.form_habitacao(request.POST)
        form4 =  self.form_cadastro(request.POST)
        forms_generic = {"Informações da Referência Familiar": form1,
                         "Informações do Endereço": form2,
                         "Informações da Moradia": form3,
                         "Informações do Cadastramento":form4}
        tecnico = Tecnico.objects.get(usuario=request.user)
        if form1.is_valid():
            if form2.is_valid():
                if form3.is_valid():
                    if form4.is_valid():
                        entrevistador = form4.cleaned_data['entrevistador']
                        abrangencia = form4.cleaned_data['abrangencia']
                        cadastro = Cadastro.objects.create(responsavel_familiar=form1.save(),
                                                        endereco=form2.save(), habitacao=form3.save(),
                                                        entrevistador=entrevistador,abrangencia=abrangencia)
                        messages.success(request, f'Cadastro Realizado Com Sucesso.')
                        return redirect('listar_cadastros', f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)



@method_decorator(login_required, name='dispatch')
class EditarCadastroView(TemplateView):

    form_cadastro = FormCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Cadastro", 'link': '/cadastros/lista/'}

    def get(self, request, *args, **kwargs):
        cadastro_bd = get_object_or_404(Cadastro,id=self.kwargs['pk'])
        forms_generic = {"Informações do Cadastramento": self.form_cadastro(instance=cadastro_bd),
                         }
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        cadastro_bd = get_object_or_404(Cadastro,id=self.kwargs['pk'])
        
        form =  self.form_cadastro(request.POST)
        forms_generic = {
                         "Informações do Cadastramento":form}
        tecnico = Tecnico.objects.get(usuario=request.user)
        
        if form.is_valid():
            atualizacao = False
            entrevistador_form = form.cleaned_data['entrevistador']
            abrangencia_form = form.cleaned_data['abrangencia']
            
            if cadastro_bd.entrevistador != entrevistador_form:
                  cadastro_bd.entrevistador = entrevistador_form
                  atualizacao = True
            if cadastro_bd.abrangencia != abrangencia_form:
                  cadastro_bd.abrangencia = abrangencia_form
                  atualizacao = True
            
            if atualizacao:
                cadastro_bd.save()
                messages.success(request, f'Cadastro Atualizado Com Sucesso.')
                return redirect('listar_cadastros', f'id:{cadastro_bd.id}')
            else:
                return redirect('listar_cadastros', f'id:{cadastro_bd.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)



@method_decorator(login_required, name='dispatch')
class EditarEnderecoView(TemplateView):
    form_endereco = FormEndereco
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Endereco"}

    def get(self, request, *args, **kwargs):
        endereco = get_object_or_404(Endereco, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(endereco=endereco)
        link = request.META.get('HTTP_REFERER')
        pprint(cadastro._meta.get_field('abrangencia').verbose_name)
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {"Informações do Endereço": self.form_endereco(instance=endereco)}

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_endereco(request.POST)
        endereco = get_object_or_404(Endereco, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(endereco=endereco)
        forms_generic = {"Informações do Endereço": form}
        if form.is_valid():
            editar_endereco(endereco, form)
            messages.success(request, f'Endereço Atualizado Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class EditHabitacaoView(TemplateView):
    form_habitacao = FormHabitacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Habitação"}

    def get(self, request, *args, **kwargs):
        habitacao = get_object_or_404(Habitacao, id=self.kwargs['pk'])
        forms_generic = {"Informações da Moradia": self.form_habitacao(instance=habitacao)}
        cadastro = Cadastro.objects.get(habitacao=habitacao)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['forms_generic'] = forms_generic

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_habitacao(request.POST)
        habitacao = get_object_or_404(Habitacao, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(habitacao=habitacao)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {"Informações do Endereço": form}
        if form.is_valid():
            habitacao.situacao_moradia = form.cleaned_data['situacao_moradia']
            habitacao.tipo_construcao = form.cleaned_data['tipo_construcao']
            habitacao.rede_eletrica = form.cleaned_data['rede_eletrica']
            habitacao.possui_abastecimento = form.cleaned_data['possui_abastecimento']
            habitacao.possui_rede_esgoto = form.cleaned_data['possui_rede_esgoto']
            habitacao.possui_coleta = form.cleaned_data['possui_coleta']
            habitacao.pavimentacao = form.cleaned_data['pavimentacao']
            habitacao.tempo_ocupacao = form.cleaned_data['tempo_ocupacao']
            habitacao.equipamento_comunitario.set(form.cleaned_data['equipamento_comunitario'])
            habitacao.numero_comodos = form.cleaned_data['numero_comodos']
            habitacao.numero_moradores = form.cleaned_data['numero_moradores']

            habitacao.save(force_update=True)
            messages.success(request, f'Dados Atualizados Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class ExibirFichaCadastroView(TemplateView):
    # form_habitacao = FormHabitacao
    template_name = "cadastros/dados_cadastro.html"
    context = {'titulo_pagina': "Dados Cadastro"}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['cadastro'] = CadastroData(cadastro)
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class EditarReferenciaView(TemplateView):
    form_referencia = FormEditarReferencia
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Referência"}

    def get(self, request, *args, **kwargs):
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações da Referência Familiar": self.form_referencia(instance=referencia), }
        cadastro_bd = Cadastro.objects.get(responsavel_familiar=referencia)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro_bd.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro_bd.id}'
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form1 = self.form_referencia(request.POST)
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações da Referência Familiar": form1}
        cadastro_bd = Cadastro.objects.get(responsavel_familiar=referencia)
        self.context['id_cancelar'] = f'id:{cadastro_bd.id}'
        if form1.is_valid():
            editar_pessoa(referencia, form1)
            messages.success(request, f'Informações Atualizadas Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro_bd.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class AdicionarHabitacaoView(TemplateView):
    form_habitacao = FormHabitacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Habitação"}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        forms_generic = {"Informações da Moradia": self.form_habitacao()}
        
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_habitacao(request.POST)
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        # cadastro = Cadastro.objects.get(habitacao=habitacao)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {"Informações do Endereço": form}
        if form.is_valid():
            habitacao = form.save()
            cadastro.habitacao = habitacao
            cadastro.save()
            messages.success(request, f'Dados Cadastrados Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class EditarHabitacaoView(TemplateView):
    form_habitacao = FormHabitacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Habitação"}

    def get(self, request, *args, **kwargs):
        habitacao = get_object_or_404(Habitacao, id=self.kwargs['pk'])
        forms_generic = {"Informações da Moradia": self.form_habitacao(instance=habitacao)}
        cadastro = Cadastro.objects.get(habitacao=habitacao)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_habitacao(request.POST)
        habitacao = get_object_or_404(Habitacao, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(habitacao=habitacao)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {"Informações do Endereço": form}
        if form.is_valid():
            habitacao.situacao_moradia = form.cleaned_data['situacao_moradia']
            habitacao.tipo_construcao = form.cleaned_data['tipo_construcao']
            habitacao.rede_eletrica = form.cleaned_data['rede_eletrica']
            habitacao.possui_abastecimento = form.cleaned_data['possui_abastecimento']
            habitacao.possui_rede_esgoto = form.cleaned_data['possui_rede_esgoto']
            habitacao.possui_coleta = form.cleaned_data['possui_coleta']
            habitacao.pavimentacao = form.cleaned_data['pavimentacao']
            habitacao.tempo_ocupacao = form.cleaned_data['tempo_ocupacao']
            habitacao.equipamento_comunitario.set(form.cleaned_data['equipamento_comunitario'])
            habitacao.numero_comodos = form.cleaned_data['numero_comodos']
            habitacao.numero_moradores = form.cleaned_data['numero_moradores']
            habitacao.save(force_update=True)
            messages.success(request, f'Dados Atualizados Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class ExibirDadosCadastroView(TemplateView):
    template_name = "cadastros/dados_cadastro.html"
    context = {'titulo_pagina': "Dados Cadastro"}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['cadastro'] = CadastroData(cadastro)

        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class AdicionarMembroView(TemplateView):
    form_membro = FormMembro
    form_dados = FormDadosCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Membro"}

    def get(self, request, *args, **kwargs):
        pk = self.get_pk()
        cadastro = get_object_or_404(Cadastro, id=pk)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {
            "Informações do Cadastro": self.form_dados(initial={'responsavel': cadastro.responsavel_familiar.nome,
                                                                'bairro': cadastro.endereco.bairro}),
            "Informações do Membro": self.form_membro()}

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_membro(request.POST)
        pk = self.get_pk()
        cadastro = get_object_or_404(Cadastro, id=pk)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {
            "Informações do Cadastro": self.form_dados(initial={'responsavel': cadastro.responsavel_familiar.nome,
                                                                'bairro': cadastro.endereco.bairro}),
            "Informações do Membro": form}
        if form.is_valid():
            salvar_membro(form, cadastro)
            messages.success(request, f'Membro Adicionado à Composição Familiar.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')


@method_decorator(login_required, name='dispatch')
class EditarMembroView(TemplateView):
    form_membro = FormEditarMembro
    form_dados = FormDadosCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Membro"}

    def get(self, request, *args, **kwargs):
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {
            "Informações do Cadastro": self.form_dados(initial={'responsavel': cadastro.responsavel_familiar.nome,
                                                                'bairro': cadastro.endereco.bairro}),
            "Informações do Membro": self.form_membro(instance=membro)}

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_membro(request.POST)
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {
            "Informações do Cadastro": self.form_dados(initial={'responsavel': cadastro.responsavel_familiar.nome,
                                                                'bairro': cadastro.endereco.bairro}),
            "Informações do Membro": form}
        if form.is_valid():
            editar_membro(membro, form)
            messages.success(request, f'Informações do Membro Atualizadas Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')


@method_decorator(login_required, name='dispatch')
class ExcluirMembroView(TemplateView):
    template_name = "cadastros/dados_excluir.html"
    context = {'titulo_pagina': "Editar Membro"}

    def get(self, request, *args, **kwargs):
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] = 'dados'
            self.context['id_cancelar'] = cadastro.id
        else:
            self.context['url_cancelar'] = 'lista'
            self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['dados_cadastro'] = cadastro
        self.context['dados_membro'] = MembroDados(membro)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['dados_cadastro'] = cadastro
        self.context['dados_membro'] = MembroDados(membro)
        # print(request.POST)
        if "confirmar" in request.POST:
            membro.delete()
            messages.success(request, f'Informações do Membro Foram Excluídas!')
            return redirect('listar_cadastros', f'id:{cadastro.id}')
        return render(request, self.template_name, self.context)

    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')


@method_decorator(login_required, name='dispatch')
class EnviarDados(TemplateView):
    form_upload = FormUploadDados
    template_name = "cadastros/forms/formulario_upload.html"
    context = {'titulo_pagina': "Enviar ", 'link': '/'}

    def get(self, request, *args, **kwargs):
        forms_generic = {"Dados": self.form_upload()}

        # self.context['data_upload'] = data_upload
        self.context["resultados"] = None
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):

        form = self.form_upload(request.POST, request.FILES)
        forms_generic = {"Informações da Solicitação": form}
        
        if form.is_valid():
            lista_erros = []
            pasta_temporaria = os.path.join(settings.BASE_DIR, "files/media/")
            arquivo = form.cleaned_data['arquivo_dados']
            nome_arquivo = str(form.cleaned_data['arquivo_dados'])
            tipo = form.cleaned_data['tipo_informacoes']
            tecnico = get_object_or_404(Tecnico, usuario=request.user)  # .objects.get()
            with open(f'{pasta_temporaria}{nome_arquivo}', 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            caminho_arquivo = os.path.join(pasta_temporaria, nome_arquivo)
            with open(caminho_arquivo, encoding='utf-8') as meu_json:
                dados = json.load(meu_json)
            if tipo == "1":
                for dado in dados:
                    try:
                        Bairro.objects.create(nome=dado['nome'])
                    except:
                        pass
            elif tipo == "2":
                print("-"*10)
                    
                for dado in dados:
                    referencia_familiar = Referencia()
                    endereco = Endereco()
                    cadastro = Cadastro()
                    validar_cpf = None
                    # print(vars(referencia_familiar))
                    for chave, valor in dado.items():
                        
                        if chave in vars(referencia_familiar):
                            if valor:   
                                if chave == "cpf":
                                    cpf_arquivo = valor.replace(".","").replace("-","")
                                    validar_cpf = is_cpf_valid(cpf_arquivo)
                                    if validar_cpf:
                                        setattr(referencia_familiar, chave, cpf_arquivo)
                                else:
                                    setattr(referencia_familiar, chave, valor)
                                
                        if chave in vars(endereco) or chave == 'bairro':
                            if valor:
                                # print(chave)
                                if chave == 'bairro':
                                    busca_bairro = Bairro.objects.filter(nome=valor)
                                    if busca_bairro:
                                        setattr(endereco, 'bairro_id', busca_bairro.get(nome=valor).id)
                                    else:
                                        bairro = Bairro.objects.create(nome=valor)
                                        # print(bairro.id)
                                        setattr(endereco, 'bairro_id', bairro.id)
                                else:
                                    setattr(endereco, chave, valor)
                        if chave in vars(cadastro):
                            if valor:
                                setattr(cadastro, chave, valor)
                    
                    if referencia_familiar.cpf and validar_cpf:
                        try:
                            referencia_familiar.save()
                            setattr(cadastro, 'responsavel_familiar_id', referencia_familiar.id)
                            try:
                                endereco.save()
                                setattr(cadastro, 'endereco_id', endereco.id)
                                
                                try:
                                    setattr(cadastro, 'responsavel_cadastro_id', tecnico.id)
                                    cadastro.save()
                                    resultado = ErrosData(referencia=f"{referencia_familiar.nome}",resultado="Salvo Com Sucesso",descricao_erro="-", erro=None)
                                    lista_erros.append(resultado)
                                
                                except Exception as e:
                                    
                                    referencia_familiar.delete()
                                    endereco.delete()
                                    resultado = ErrosData(referencia=f"{referencia_familiar.nome}",resultado="Erro ao Salvar",
                                                                descricao_erro="Erro não documentado", erro=str(e))
                                    lista_erros.append(resultado)
                                    
                            except Exception as e:
                                referencia_familiar.delete()
                                resultado = ErrosData(referencia=f"{referencia_familiar.nome}",resultado="Erro ao Salvar",
                                                            descricao_erro="Erro não documentado", erro=str(e))
                                lista_erros.append(resultado)
                        except Exception as e:
                            if str(e) == "UNIQUE constraint failed: cadastros_pessoa.cpf":
                                resultado = ErrosData(referencia=f"{referencia_familiar.nome}",resultado="Erro ao Salvar",
                                                        descricao_erro="CPF já está cadastrado", erro=str(e))
                                lista_erros.append(resultado)
                            else:
                                resultado = ErrosData(referencia=f"{referencia_familiar.nome}",resultado="Erro ao Salvar",
                                                        descricao_erro="Erro não documentado", erro=str(e))
                                lista_erros.append(resultado)
                    else:
                        resultado = ErrosData(referencia=f"{referencia_familiar.nome}",resultado="Erro ao Salvar",
                                                        descricao_erro="CPF inválido ou já cadastrado", erro="Validação")
                        lista_erros.append(resultado)

                    # print(vars(referencia_familiar))
                    # print(vars(endereco))
                    # print(vars(cadastro))

            os.remove(caminho_arquivo)
        self.context["resultados"] = lista_erros
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


def dados_cadastro_json(request):
    data_json = []
    lista = list(Cadastro.objects.values()) + list(Referencia.objects.values())
    data_json.append(lista)
    # data_json.append(list())

    return JsonResponse(data_json, safe=False)


def handler500(request):
    return render(request, '500.html')


def handler404(request, exception):
    return render(request, '404.html')
