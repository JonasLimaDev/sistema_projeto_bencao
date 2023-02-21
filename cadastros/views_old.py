from django.shortcuts import render, redirect
from .forms import *
from .services import *  # , inserir_bairros
from .entidades import dados
from .models import *
# from tecnicos.models import Tecnico
from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from random import randint
import os, json
from django.conf import settings
from pprint import pprint

def gerar_valores(mes_dict):
    for mes in mes_dict:
        mes_dict[mes]= randint(20, 249)
    return mes_dict


class HomePageView(TemplateView):
    template_name = 'base.html'

    def get(self,request,*args, **kwargs):
        dados= {}
        inserir_bairros()
        # orgs = ["CRAS I","CRAS II","CRAS III","CREAS","SEMAPS - SEDE","Projeto"]
        # for org in orgs:
        #     mes = {'Jan':0, "Fev":0,'Mar':0, "Abr":0,
        # 'Mai':0,"Jun":0,'Jul':0, "Ago":0,
        # 'Set':0, "Out":0,'Nov':0, "Dez":0,}
        #     lista = gerar_valores(mes)
        #     dados[org]=lista
        return render(request, self.template_name,{'dados':dados})



#@method_decorator(login_required, name='dispatch')
class ListaCadastroView(TemplateView):
    template_name = 'cadastros/lista_cadastros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        argumento = None

        if 'filter' in self.kwargs:
            argumento = self.kwargs['filter']
            if "name" in argumento:
                argumento = argumento.split(':')
            elif "id" in argumento:
                argumento = argumento.split(':')
            elif "cpf" in argumento:
                argumento = argumento.split(':')

        if argumento:
            lista_cadastro = []
            if argumento[0] =='name':
                lista_cadastro = buscar_cadastro_nome(argumento[1])
            elif argumento[0] =='cpf':
                lista_cadastro = buscar_cadastro_cpf(argumento[1])
            elif argumento[0] =='id':
                lista_cadastro.append(get_object_or_404(Cadastro, id=argumento[1]))

            context['cadastros'] = [dados.Cadastro(cadastro_bd) for cadastro_bd in lista_cadastro]
        else:
            context['cadastros'] = [dados.Cadastro(cadastro_bd) for cadastro_bd in Cadastro.objects.all()]
        return context

    # #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        busca = request.POST['busca']
        if busca:
            if len(busca) == 11 and busca.isdigit():
                return redirect('listar_cadastros', "cpf:" + request.POST['busca'])
            elif busca.isdigit():
                return redirect('listar_cadastros', "id:" + request.POST['busca'])
            else:
                return redirect('listar_cadastros', "name:" + request.POST['busca'])
        else:
            return redirect('listar_cadastros')



#@method_decorator(login_required, name='dispatch')
class AdicionarCadastroView(TemplateView):
    form_referencia = FormReferencia
    form_endereco = FormEndereco
    form_habitacao = FormHabitacao

    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Adicionar Cadastro",'link':'/cadastros/lista/'}

    def get(self, request, *args, **kwargs):
        # inserir_bairros()
        forms_generic = {"Informações da Referência Familiar": self.form_referencia(),
                         "Informações de Endereço": self.form_endereco(),
                         "Informações da Moradia": self.form_habitacao()}
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form1 = self.form_referencia(request.POST)
        form2 = self.form_endereco(request.POST)
        form3 = self.form_habitacao(request.POST)
        forms_generic = {"Informações da Referência Familiar": form1,
                         "Informações do Endereço": form2,
                         "Informações da Moradia": form3}
        # tecnico = Tecnico.objects.get(usuario=request.user)
        if form1.is_valid():
            if form2.is_valid():
                if form3.is_valid():
                    cadastro = Cadastro.objects.create(responsavel_familiar=form1.save(),
                        endereco=form2.save(), situacao_habitacao=form3.save())
                    messages.success(request, f'Cadastro Realizado Com Sucesso.')
                    return redirect('listar_cadastros',f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)



#@method_decorator(login_required, name='dispatch')
class EditarReferenciaView(TemplateView):
    form_referencia = FormEditarReferencia
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Referência"}

    def get(self, request, *args, **kwargs):
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações da Referência Familiar": self.form_referencia(instance=referencia),}
        cadastro_bd = Cadastro.objects.get(responsavel_familiar=referencia)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  cadastro_bd.id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{cadastro_bd.id}'
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form1 = self.form_referencia(request.POST)
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações da Referência Familiar": form1}
        cadastro_bd = Cadastro.objects.get(responsavel_familiar=referencia)
        self.context['id_cancelar'] = f'id:{cadastro_bd.id}'
        if form1.is_valid():
            referencia_bd = editar_pessoa(referencia,form1)
            messages.success(request, f'Informações Atualizadas Com Sucesso.')
            return redirect('listar_cadastros',f'id:{cadastro_bd.id}')

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
        cadastro = Cadastro.objects.get(responsavel_familiar__documentos_extras=dados_bd)
        dados_bd = get_object_or_404(Identificacao, id=self.kwargs['pk'])
        self.context['url_cancelar'] = ''
        print(dados_bd.rg)
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


class ExibirDadosCadastroView(TemplateView):
    # form_habitacao = FormHabitacao
    template_name = "cadastros/dados_cadastro.html"
    context = {'titulo_pagina': "Dados Cadastro"}

    def get(self, request, *args, **kwargs):
        cadastro = get_object_or_404(Cadastro, id=self.kwargs['pk'])
        # forms_generic = {"Informações da Moradia": self.form_habitacao(instance=habitacao)}
        # for fieldname in forms_generic["Informações da Moradia"].fields:
        #     forms_generic["Informações da Moradia"].fields[fieldname].disabled = True
        # cadastro = Cadastro.objects.get(situacao_habitacao=habitacao)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['cadastro'] = dados.Cadastro(cadastro)
        
        
        return render(request, self.template_name, self.context)

 

#@method_decorator(login_required, name='dispatch')
class AdicionarMembroView(TemplateView):
    form_membro = FormEditarMembro
    form_dados = FormDadosCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Membro"}
    def get(self, request, *args, **kwargs):
        pk = self.get_pk()
        cadastro = get_object_or_404(Cadastro, id=pk)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  cadastro.id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{cadastro.id}'
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
            return redirect('listar_cadastros',f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')


#@method_decorator(login_required, name='dispatch')
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
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  cadastro.id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{cadastro.id}'
        forms_generic = {"Informações do Cadastro": self.form_dados(initial={'responsavel':cadastro.responsavel_familiar.nome,
                                                                             'bairro':cadastro.endereco.bairro}),
                         "Informações do Membro": self.form_membro(instance=membro)}

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):
        form = self.form_membro(request.POST)
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        forms_generic = {"Informações do Cadastro": self.form_dados(initial={'responsavel':cadastro.responsavel_familiar.nome,
                                                                             'bairro':cadastro.endereco.bairro}),
                         "Informações do Membro": form}
        if form.is_valid():
            editar_membro(membro, form)
            messages.success(request, f'Informações do Membro Atualizadas Com Sucesso.')
            return redirect('listar_cadastros',f'id:{cadastro.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')


#@method_decorator(login_required, name='dispatch')
class ExcluirMembroView(TemplateView):
    # form_membro = FormEditarMembro
    # form_dados = FormDadosCadastro
    template_name = "cadastros/dados_excluir.html"
    context = {'titulo_pagina': "Editar Membro"}
    def get(self, request, *args, **kwargs):
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        link = request.META.get('HTTP_REFERER')
        if "exibir" in link:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  cadastro.id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{cadastro.id}'
        # forms_generic = {"Informações do Cadastro": self.form_dados(initial={'responsavel':cadastro.responsavel_familiar.nome,
        #                                                                      'bairro':cadastro.endereco.bairro}),
        #                  "Informações do Membro": self.form_membro(instance=membro)}

        # self.context['forms_generic'] = forms_generic
        self.context['dados_cadastro'] = cadastro
        self.context['dados_membro'] = dados.Membro(membro)
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):
        # form = self.form_membro(request.POST)
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)
        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['dados_cadastro'] = cadastro
        self.context['dados_membro'] = Memembro
        print(request.POST)
        if "confirmar" in request.POST:
            membro.delete()
            messages.success(request, f'Informações do Membro Foram Excluídas!')
            return redirect('listar_cadastros',f'id:{cadastro.id}')
        # forms_generic = {"Informações do Cadastro": self.form_dados(initial={'responsavel':cadastro.responsavel_familiar.nome,
        #                                                                      'bairro':cadastro.endereco.bairro}),
        #                  "Informações do Membro": form}
        # if form.is_valid():
        #     editar_membro(membro, form)
        #     messages.success(request, f'Informações do Menbro Atualizadas Com Sucesso.')
        #     

        # self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')



#@method_decorator(login_required, name='dispatch')
class EnviarDados(TemplateView):
    form_upload = FormUploadDados
    template_name = "modelos/formulario_beneficios.html"
    context = {'titulo_pagina': "Enviar ",'link':'/'}
    def get(self, request, *args, **kwargs):
        forms_generic = {"Dados": self.form_upload()}
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        
        form = self.form_upload(request.POST,request.FILES)
        forms_generic = {"Informações da Solicitação": form}
    
        if form.is_valid():
            pasta_temporaria = os.path.join(settings.BASE_DIR, "media/")
            arquivo = form.cleaned_data['arquivo_dados']
            nome_arquivo = str(form.cleaned_data['arquivo_dados'])
            tipo = form.cleaned_data['tipo_informacoes']
            tecnico = get_object_or_404(Tecnico,usuario=request.user) #.objects.get()
            print(tecnico.cargo)
            with open(f'{pasta_temporaria}{nome_arquivo}', 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            caminho_arquivo = os.path.join(pasta_temporaria, nome_arquivo)
            with open(caminho_arquivo, encoding='utf-8') as meu_json:
                dados = json.load(meu_json)
            if tipo == "1":
                for dado in dados:
                    # print(dado['nome'])
                    try:
                        Bairro.objects.create(nome=dado['nome'])
                    except:
                        pass
            else:
                for dado in dados:
                    print(tecnico)
                    # salvar_cadastros_massivo(dado, tecnico)
            #return redirect('avaliar_solicitacao',registro.id)
            os.remove(caminho_arquivo)
            
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)
 



def handler500(request):
    return render(request,'500.html')


def handler404(request, exception):
    return render(request,'404.html')
