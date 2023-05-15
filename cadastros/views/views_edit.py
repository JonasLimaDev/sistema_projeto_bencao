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

@method_decorator(login_required, name='dispatch')
class EditCadastroView(TemplateView):
    form_cadastro = FormCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Cadastro", 'link': '/cadastros/lista/'}

    def get(self, request, *args, **kwargs):
        cadastro_bd = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        forms_generic = {"Informações do Cadastramento": self.form_cadastro(instance=cadastro_bd),
                         }
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        cadastro_bd = get_object_or_404(Cadastro, id=self.kwargs['pk'])

        form = self.form_cadastro(request.POST)
        forms_generic = {"Informações do Cadastramento": form}
        tecnico = Tecnico.objects.get(usuario=request.user)

        if form.is_valid():
            atualizacao = False
            entrevistador_form = form.cleaned_data['entrevistador']
            abrangencia_form = form.cleaned_data['abrangencia']
            lista_alteracoes = []
            dict_data_form = dict(form.fields["abrangencia"]._choices)
            if cadastro_bd.entrevistador != entrevistador_form:
                lista_alteracoes.append(ChangeCampoData(campo="Entrevistador", valor_antigo=cadastro_bd.entrevistador,
                                                        valor_novo=entrevistador_form))
                cadastro_bd.entrevistador = entrevistador_form
                atualizacao = True
            if cadastro_bd.abrangencia != abrangencia_form:
                lista_alteracoes.append(ChangeCampoData(campo="Abrangência", valor_antigo=cadastro_bd.get_abrangencia_display(),
                                                        valor_novo=dict_data_form[form.cleaned_data["abrangencia"]]))
                cadastro_bd.abrangencia = abrangencia_form
                atualizacao = True

            if atualizacao:
                cadastro_bd.save()
                create_change_campos(lista_alteracoes, tecnico, 'cadastro', cadastro_bd.id, str(cadastro_bd))

                messages.success(request, f'Cadastro Atualizado Com Sucesso.')
                return redirect('listar_cadastros', f'id:{cadastro_bd.id}')
            else:
                return redirect('listar_cadastros', f'id:{cadastro_bd.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class EditEnderecoView(TemplateView):
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
        tecnico = Tecnico.objects.get(usuario=request.user)
        if form.is_valid():
            atualizacao, lista_alteracoes = editar_model_data(endereco, form)
            if atualizacao:
                create_change_campos(lista_alteracoes, tecnico, 'endereco', endereco.id, str(cadastro))
                messages.success(request, f'Endereço Atualizado Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class EditReferenciaView(TemplateView):
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
        tecnico = Tecnico.objects.get(usuario=request.user)
        if form1.is_valid():

            atualizacao, lista_alteracoes = editar_model_data(referencia, form1)
            if atualizacao:
                create_change_campos(lista_alteracoes, tecnico, 'referencia', referencia.id, str(referencia))
                messages.success(request, f'Informações Atualizadas Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro_bd.id}')

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
        tecnico = Tecnico.objects.get(usuario=request.user)
        if form.is_valid():
            # editar_model_data(habitacao,form)
            atualizacao, lista_alteracoes = editar_model_data(habitacao, form, ["equipamento_comunitario"])

            # Converte em lista os dados da relação N:N
            lista_equipamentos_form = [item for item in form.cleaned_data['equipamento_comunitario']]
            lista_equipamentos_bd = [item for item in habitacao.equipamento_comunitario.all()]

            if lista_equipamentos_form != lista_equipamentos_bd:
                """Verifica se as listas são diferentes para gerar alteração"""
                equipamentos_str_bd = lista_objeto_str(lista_equipamentos_bd)
                equipamentos_str_form = lista_objeto_str(lista_equipamentos_form)
                habitacao.equipamento_comunitario.set(form.cleaned_data['equipamento_comunitario'])
                atualizacao = True
                lista_alteracoes.append(ChangeCampoData(campo="Equipamentos Comunitários Próximos",
                                                        valor_antigo=equipamentos_str_bd if equipamentos_str_bd else "-",
                                                        valor_novo=equipamentos_str_form))
                habitacao.save()
            if atualizacao:
                create_change_campos(lista_alteracoes, tecnico, 'Dados Habitacionais', habitacao.id, str(cadastro))
                messages.success(request, f'Dados Atualizados Com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class EditMembroView(TemplateView):
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
        tecnico = Tecnico.objects.get(usuario=request.user)
        forms_generic = {
            "Informações do Cadastro": self.form_dados(initial={'responsavel': cadastro.responsavel_familiar.nome,
                                                                'bairro': cadastro.endereco.bairro}),
            "Informações do Membro": form}
        if form.is_valid():
            atualizacao, lista_alteracoes = editar_model_data(membro, form)
            if atualizacao:
                create_change_campos(lista_alteracoes, tecnico, 'membro', membro.id, str(membro))
                messages.success(request, f'Informações do Membro Atualizadas Com Sucesso.')

            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')

