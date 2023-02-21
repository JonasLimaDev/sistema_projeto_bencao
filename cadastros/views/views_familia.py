from ..models import Cadastro, Referencia, Membros

from ..forms import FormEditarReferencia, FormEditarMembro, FormDadosCadastro,FormMembro

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView
from django.contrib import messages
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required

from ..services import editar_pessoa, editar_membro, salvar_membro
from ..entidades import dados
#@method_decorator(login_required, name='dispatch')
class EditarReferenciaView(TemplateView):
    form_referencia = FormEditarReferencia
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Referência"}
    

    def get(self, request, *args, **kwargs):
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações da Referência Familiar": self.form_referencia(instance=referencia),}
        cadastro_bd = Cadastro.objects.get(responsavel_familiar=referencia)

        self.url_retorno(request,cadastro_bd.id)

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form1 = self.form_referencia(request.POST)
        referencia = get_object_or_404(Referencia, id=self.kwargs['pk'])
        forms_generic = {"Informações da Referência Familiar": form1}
        cadastro_bd = Cadastro.objects.get(responsavel_familiar=referencia)
        
        self.url_retorno(request, cadastro_bd.id)

        if form1.is_valid():
            referencia_bd = editar_pessoa(referencia,form1)
            messages.success(request, f'Informações Atualizadas Com Sucesso.')
            return redirect('listar_cadastros',f'id:{cadastro_bd.id}')

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)
    
    def url_retorno(self,request,id):

        url_anterior = request.META.get('HTTP_REFERER')
        if 'editar' not in url_anterior or 'adicionar' not in url_anterior  :
            request.session['retorno'] = request.META.get('HTTP_REFERER')  

        if "exibir" in request.session['retorno']:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{id}'

    


#@method_decorator(login_required, name='dispatch')
class AdicionarMembroView(TemplateView):
    form_membro = FormMembro
    form_dados = FormDadosCadastro
    template_name = "cadastros/forms/formulario_cadastro.html"
    context = {'titulo_pagina': "Editar Membro"}
    def get(self, request, *args, **kwargs):
        pk = self.get_pk()
        cadastro = get_object_or_404(Cadastro, id=pk)
        self.url_retorno(request, cadastro.id)
        forms_generic = {
            "Informações do Cadastro": self.form_dados(initial={'responsavel': cadastro.responsavel_familiar.nome,
                                                                'bairro': cadastro.endereco.bairro}),
            "Informações do Membro": self.form_membro()
            }

        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):
        form = self.form_membro(request.POST)
        pk = self.get_pk()
        cadastro = get_object_or_404(Cadastro, id=pk)
        self.url_retorno(request, cadastro.id)
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
        
    def url_retorno(self,request,id):

        url_anterior = request.META.get('HTTP_REFERER')
        if 'editar' not in url_anterior or 'adicionar' not in url_anterior  :
            request.session['retorno'] = request.META.get('HTTP_REFERER')  
            
        if "exibir" in request.session['retorno']:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{id}'

    


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
        self.url_retorno(request, cadastro.id)
       
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
        self.url_retorno(request, cadastro.id)
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
        
    def url_retorno(self,request,id):

        url_anterior = request.META.get('HTTP_REFERER')
        if 'editar' not in url_anterior or 'adicionar' not in url_anterior  :
            request.session['retorno'] = request.META.get('HTTP_REFERER')  
            
        if "exibir" in request.session['retorno']:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{id}'

    


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
        self.url_retorno(request, cadastro.id)
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
        self.context['dados_membro'] = membro
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
    
        
    def url_retorno(self,request,id):

        url_anterior = request.META.get('HTTP_REFERER')
        if 'editar' not in url_anterior or 'adicionar' not in url_anterior  :
            request.session['retorno'] = request.META.get('HTTP_REFERER')  
            
        if "exibir" in request.session['retorno']:
            self.context['url_cancelar'] =  'dados'
            self.context['id_cancelar'] =  id
        else:
            self.context['url_cancelar'] =  'lista'
            self.context['id_cancelar'] =  f'id:{id}'

    
