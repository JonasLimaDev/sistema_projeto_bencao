from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from cadastros.models import Cadastro, Referencia, Pessoa

from ..models import Identificacao,  Educacao, Saude, DadosBanco
from ..forms import FormInfoExtra, FormDadosEducacao, FormDadosSaude, FormDadosBancarios

@method_decorator(login_required, name='dispatch')
class EditExtrasView(TemplateView):
    form_extra = FormInfoExtra
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Adicionais", 'url_cancelar': 'dados'}
    def get(self, request, *args, **kwargs):
        dados_bd = get_object_or_404(Identificacao, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(responsavel_familiar__documentos_extras=dados_bd)

        self.context['id_cancelar'] = cadastro.id
        forms_generic = {"Informações Extras": self.form_extra(instance=dados_bd)}
        # self.context['cadastro'] = cadastro
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_extra(request.POST)
        # cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        # self.context['id_cancelar'] = f'id:{cadastro.id}'
        dados_bd = get_object_or_404(Identificacao, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(responsavel_familiar__documentos_extras=dados_bd)

        self.context['url_cancelar'] = ''
        referencia = Referencia.objects.get(documentos_extras=dados_bd)
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            dados_bd.rg = form.cleaned_data['rg']
            dados_bd.orgao_emissor = form.cleaned_data['orgao_emissor']
            dados_bd.data_emissao = form.cleaned_data['data_emissao']
            dados_bd.titulo_eleitor = form.cleaned_data['titulo_eleitor']
            dados_bd.zona = form.cleaned_data['zona']
            dados_bd.secao = form.cleaned_data['secao']
            dados_bd.natural_cidade = form.cleaned_data['natural_cidade']
            dados_bd.natural_estado = form.cleaned_data['natural_estado']
            dados_bd.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('listar_cadastros', f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)



@method_decorator(login_required, name='dispatch')
class EditDadosEducacaoView(TemplateView):
    form_educacao = FormDadosEducacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        dados_bd = get_object_or_404(Educacao, id=self.kwargs['pk'])
        forms_generic = {"Informações Extras": self.form_educacao(instance=dados_bd)}
        self.context['id_cancelar'] = self.kwargs['sk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_educacao(request.POST)
        dados_bd = get_object_or_404(Educacao, id=self.kwargs['pk'])

        self.context['id_cancelar'] = self.kwargs['sk']
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            dados_bd.estuda = form.cleaned_data['estuda']
            dados_bd.nivel_curso = form.cleaned_data['nivel_curso']
            dados_bd.local = form.cleaned_data['local']
            dados_bd.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['sk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)



@method_decorator(login_required, name='dispatch')
class EditDadosSaudeView(TemplateView):
    form_saude = FormDadosSaude
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        dados_bd = get_object_or_404(Saude, id=self.kwargs['pk'])
        forms_generic = {"Informações Extras": self.form_saude(instance=dados_bd)}
        self.context['id_cancelar'] = self.kwargs['sk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_saude(request.POST)
        dados_bd = get_object_or_404(Educacao, id=self.kwargs['pk'])

        self.context['id_cancelar'] = self.kwargs['sk']
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            dados_bd.deficiencia = form.cleaned_data['deficiencia']
            dados_bd.tipo_deficiencia = form.cleaned_data['tipo_deficiencia']
            dados_bd.gravidez = form.cleaned_data['gravidez']
            dados_bd.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['sk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)



@method_decorator(login_required, name='dispatch')
class EditDadosBancariosView(TemplateView):
    form_banco = FormDadosBancarios
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar': 'dados'}

    def get(self, request, *args, **kwargs):
        dados_bd = get_object_or_404(DadosBanco, id=self.kwargs['pk'])
        forms_generic = {"Informações Bancárias": self.form_banco(instance=dados_bd)}
        self.context['id_cancelar'] = self.kwargs['sk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_saude(request.POST)
        dados_bd = get_object_or_404(Educacao, id=self.kwargs['pk'])

        self.context['id_cancelar'] = self.kwargs['sk']
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            dados_bd.deficiencia = form.cleaned_data['deficiencia']
            dados_bd.tipo_deficiencia = form.cleaned_data['tipo_deficiencia']
            dados_bd.gravidez = form.cleaned_data['gravidez']
            dados_bd.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['sk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

