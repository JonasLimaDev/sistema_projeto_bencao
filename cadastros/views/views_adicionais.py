from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .. models import Cadastro, Endereco,Habitacao, Referencia, Identificacao, Pessoa, DadosEducacao
from ..forms import FormEndereco, FormInfoExtra, FormHabitacao, FormDadosEducacao
from ..services import editar_endereco, inserir_bairros


class HomePageView(TemplateView):
    template_name = 'base.html'

    def get(self,request,*args, **kwargs):
        dados= {}
        # inserir_bairros()
        # orgs = ["CRAS I","CRAS II","CRAS III","CREAS","SEMAPS - SEDE","Projeto"]
        # for org in orgs:
        #     mes = {'Jan':0, "Fev":0,'Mar':0, "Abr":0,
        # 'Mai':0,"Jun":0,'Jul':0, "Ago":0,
        # 'Set':0, "Out":0,'Nov':0, "Dez":0,}
        #     lista = gerar_valores(mes)
        #     dados[org]=lista
        return render(request, self.template_name,{'dados':dados})





#@method_decorator(login_required, name='dispatch')
class EditarEnderecoView(TemplateView):
    form_endereco = FormEndereco
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Endereco"}

    def get(self, request, *args, **kwargs):
        endereco = get_object_or_404(Endereco, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(endereco=endereco)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  cadastro.id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{cadastro.id}'
        forms_generic = {"Informações do Endereço": self.form_endereco(instance=endereco) }

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_endereco(request.POST)
        endereco = get_object_or_404(Endereco, id=self.kwargs['pk'])
        cadastro = Cadastro.objects.get(endereco=endereco)
        # self.context['url_cancelar'] = f"'exibir_dados_cadastro' {cadastro.id}"
        forms_generic = {"Informações do Endereço": form}
        if form.is_valid():
            editar_endereco(endereco,form)
            messages.success(request, f'Endereço Atualizado Com Sucesso.')
            return redirect('listar_cadastros',f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


#@method_decorator(login_required, name='dispatch')
class AdicinarExtrasView(TemplateView):
    form_extra = FormInfoExtra
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Adicionais", 'url_cancelar':'dados'}

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
            # editar_endereco(endereco,form)
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('listar_cadastros',f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


class EditarExtrasView(TemplateView):
    form_extra = FormInfoExtra
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Adicionais", 'url_cancelar':'dados'}
    # dados_bd = None

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
        # print(dados_bd.rg)
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
        #     # extra = form.save()
        #     # referencia.documentos_extras = extra
        #     # referencia.save()

        #     # editar_endereco(endereco,form)
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('listar_cadastros',f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


class AddDadosEducacaoView(TemplateView):
    form_educacao = FormDadosEducacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar':'dados'}

    def get(self, request, *args, **kwargs):
        print(self.kwargs['pk'])
        print(self.kwargs['sk'])

        pessoa = get_object_or_404(Pessoa, id=self.kwargs['sk'])
        forms_generic = {"Informações Extras": self.form_educacao}
        self.context['id_cancelar'] = self.kwargs['pk'] 
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_educacao(request.POST)
        pessoa = get_object_or_404(Pessoa, id=self.kwargs['sk'])
        # self.context['id_cancelar'] = cadastro.id
        # referencia = Referencia.objects.get(id=cadastro.responsavel_familiar.id)
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            educacao = form.save()
            pessoa.dados_educacionais = educacao
            pessoa.save()
            # editar_endereco(endereco,form)
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['pk'])

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


class EditDadosEducacaoView(TemplateView):
    form_educacao = FormDadosEducacao
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Informações Educacionais", 'url_cancelar':'dados'}

    def get(self, request, *args, **kwargs):
        dados_bd = get_object_or_404(DadosEducacao, id=self.kwargs['pk'])
        forms_generic = {"Informações Extras": self.form_educacao(instance=dados_bd)}
        self.context['id_cancelar'] = self.kwargs['sk']
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_educacao(request.POST)
        dados_bd = get_object_or_404(DadosEducacao, id=self.kwargs['pk'])

        self.context['id_cancelar'] = self.kwargs['sk']
        # referencia = Referencia.objects.get(id=cadastro.responsavel_familiar.id)
        forms_generic = {"Informações Extras": form}
        if form.is_valid():
            dados_bd.estuda = form.cleaned_data['estuda']
            dados_bd.nivel_curso = form.cleaned_data['nivel_curso']
            dados_bd.local = form.cleaned_data['local']
            dados_bd.save()
            messages.success(request, f'Informações Salvas com Sucesso.')
            return redirect('exibir_dados_cadastro', self.kwargs['sk'] )

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)





#@method_decorator(login_required, name='dispatch')
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
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  cadastro.id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{cadastro.id}'
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
                return redirect('listar_cadastros',f'id:{cadastro.id}')

            self.context['forms_generic'] = forms_generic
            return render(request, self.template_name, self.context)



def handler500(request):
    return render(request,'500.html')


def handler404(request, exception):
    return render(request,'404.html')
