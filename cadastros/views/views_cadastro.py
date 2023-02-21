from django.shortcuts import render, redirect

from ..models import Cadastro
from ..forms import FormReferencia, FormEndereco, FormHabitacao

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404

from ..services import buscar_cadastro_cpf, buscar_cadastro_nome

from ..entidades import dados
import re


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
            if argumento[0] == 'name':
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
        padrao = re.compile("[0-9]{3}[.]?[0-9]{3}[.]?[0-9]{3}[-]?[0-9]{2}")
        resultado = padrao.search(busca)
        if busca:
            if len(busca) == 11 and busca.isdigit() or resultado:
                busca = busca.replace('.','')
                busca = busca.replace('-','')
                print(busca)
                return redirect('listar_cadastros', "cpf:" + busca)
            # elif busca.isdigit():
            #     return redirect('listar_cadastros', "id:" + request.POST['busca'])
            else:
                return redirect('listar_cadastros', "name:" + + busca)
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
                        endereco=form2.save(), habitacao=form3.save())
                    messages.success(request, f'Cadastro Realizado Com Sucesso.')
                    return redirect('listar_cadastros',f'id:{cadastro.id}')
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


class ExibirFichaCadastroView(TemplateView):
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

