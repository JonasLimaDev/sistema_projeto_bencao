from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tecnicos.models import Tecnico
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from ..forms import *
from ..services import *
from ..filters import *

@method_decorator(login_required, name='dispatch')
class AddCadastroView(TemplateView):
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
        form4 = self.form_cadastro(request.POST)
        forms_generic = {"Informações da Referência Familiar": form1,
                         "Informações do Endereço": form2,
                         "Informações da Moradia": form3,
                         "Informações do Cadastramento": form4}
        tecnico = Tecnico.objects.get(usuario=request.user)
        if form1.is_valid():
            if form2.is_valid():
                if form3.is_valid():
                    if form4.is_valid():
                        entrevistador = form4.cleaned_data['entrevistador']
                        abrangencia = form4.cleaned_data['abrangencia']
                        cadastro = Cadastro.objects.create(responsavel_familiar=form1.save(),
                                                           endereco=form2.save(), habitacao=form3.save(),
                                                           entrevistador=entrevistador, abrangencia=abrangencia)
                        messages.success(request, f'Cadastro Realizado Com Sucesso.')
                        return redirect('listar_cadastros', f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class AddHabitacaoView(TemplateView):
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
class AddMembroView(TemplateView):
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
