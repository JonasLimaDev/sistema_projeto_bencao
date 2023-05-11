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
class UploadDados(TemplateView):
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
            pasta_temporaria = os.path.join(settings.BASE_DIR, "assets/files/media/")
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
                for dado in dados:
                    referencia_familiar = Referencia()
                    endereco = Endereco()
                    cadastro = Cadastro()
                    validar_cpf = None

                    for chave, valor in dado.items():

                        if chave in vars(referencia_familiar):
                            if valor:
                                if chave == "cpf":
                                    cpf_arquivo = valor.replace(".", "").replace("-", "")
                                    validar_cpf = is_cpf_valid(cpf_arquivo)
                                    cpf_existente = cpf_existing(cpf_arquivo)
                                    if validar_cpf:
                                        setattr(referencia_familiar, chave, cpf_arquivo)
                                else:
                                    setattr(referencia_familiar, chave, valor)

                        if chave in vars(endereco) or chave == 'bairro':
                            if valor:
                                if chave == 'bairro':
                                    busca_bairro = Bairro.objects.filter(nome=valor)
                                    if busca_bairro:
                                        setattr(endereco, 'bairro_id', busca_bairro.get(nome=valor).id)
                                    else:
                                        bairro = Bairro.objects.create(nome=valor)
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
                                    resultado = ErrosData(referencia=f"{referencia_familiar.nome}",
                                                          resultado="Salvo Com Sucesso", descricao_erro="-", erro=None)
                                    lista_erros.append(resultado)

                                except Exception as e:

                                    referencia_familiar.delete()
                                    endereco.delete()
                                    resultado = ErrosData(referencia=f"{referencia_familiar.nome}",
                                                          resultado="Erro ao Salvar Cadastro",
                                                          descricao_erro="Erro não documentado", erro=str(e))
                                    lista_erros.append(resultado)

                            except Exception as e:
                                referencia_familiar.delete()
                                resultado = ErrosData(referencia=f"{referencia_familiar.nome}",
                                                      resultado="Erro ao Salvar Endereço",
                                                      descricao_erro="Erro não documentado", erro=str(e))
                                lista_erros.append(resultado)
                        except Exception as e:
                            print(e)
                            if str(e) == "UNIQUE constraint failed: cadastros_pessoa.cpf":
                                resultado = ErrosData(referencia=f"{referencia_familiar.nome}",
                                                      resultado="Erro ao Salvar Referência",
                                                      descricao_erro="CPF já está cadastrado", erro=str(e))
                                lista_erros.append(resultado)
                            else:
                                resultado = ErrosData(referencia=f"{referencia_familiar.nome}",
                                                      resultado="Erro ao Salvar Referência",
                                                      descricao_erro="Erro não documentado", erro=str(e))
                                lista_erros.append(resultado)
                    else:
                        if cpf_existente:
                            resultado = ErrosData(referencia=f"{referencia_familiar.nome}", resultado="Erro ao Salvar Referência",
                                                descricao_erro="CPF já cadastrado", erro="Validação")
                        else:
                            
                            resultado = ErrosData(referencia=f"{referencia_familiar.nome}", resultado="Erro ao Salvar Referência",
                                                descricao_erro="CPF inválido", erro="Validação")
                        lista_erros.append(resultado)
            os.remove(caminho_arquivo)
        self.context["resultados"] = lista_erros
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)


def get_dados_json(request):
    data_json = []
    lista = list(Cadastro.objects.values()) + list(Referencia.objects.values())
    data_json.append(lista)
    # data_json.append(list())

    return JsonResponse(data_json, safe=False)


def handler500(request):
    return render(request, '500.html')


def handler404(request, exception):
    return render(request, 'base_templates/404.html')
