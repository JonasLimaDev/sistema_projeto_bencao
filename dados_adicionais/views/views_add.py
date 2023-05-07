from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from cadastros.models import Cadastro, Referencia, Pessoa

from ..forms import FormInfoExtra, FormDadosEducacao, FormDadosSaude, FormDadosBancarios

@method_decorator(login_required, name='dispatch')
class AddExtrasView(TemplateView):
    form_extra = FormInfoExtra
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Adicionais", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        forms_generic = {"Informações Extras": self.form_extra}
        self.context['id_cancelar'] = cadastro.id
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_extra(request.POST)
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        self.context['id_cancelar'] = cadastro.id
        referencia = Referencia.objects.get(id=cadastro.responsavel_familiar.id)
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            extra = form.save()
            referencia.documentos_extras = extra
            referencia.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class AddDadosEducacaoView(TemplateView):
    form_educacao = FormDadosEducacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        pessoa = get_object_or_404(Pessoa, id=self.kwargs['sk'])
        forms_generic = {"Informações Extras": self.form_educacao}
        self.context['id_cancelar'] = self.kwargs['pk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_educacao(request.POST)
        pessoa = get_object_or_404(Pessoa, id=self.kwargs['sk'])
        self.context['id_cancelar'] = self.kwargs['pk']
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            educacao = form.save()
            pessoa.dados_educacionais = educacao
            pessoa.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['pk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class AddDadosSaudeView(TemplateView):
    form_saude = FormDadosSaude
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        pessoa = get_object_or_404(Pessoa, id=self.kwargs['sk'])
        forms_generic = {"Informações Extras": self.form_saude}
        self.context['id_cancelar'] = self.kwargs['pk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_saude(request.POST)
        pessoa = get_object_or_404(Pessoa, id=self.kwargs['sk'])
        self.context['id_cancelar'] = self.kwargs['pk']
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            saude = form.save()
            pessoa.dados_saude = saude
            pessoa.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['pk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class AddDadosBancariosView(TemplateView):
    form_banco = FormDadosBancarios
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Bancárias", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações Bancárias": self.form_banco}
        self.context['id_cancelar'] = self.kwargs['pk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_banco(request.POST)
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        self.context['id_cancelar'] = self.kwargs['pk']
        forms_generic = {"Informações Bancárias": form}
        if form.is_valid():
            dados_bancarios = form.save()
            referencia.dados_bancarios = dados_bancarios
            referencia.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['pk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

