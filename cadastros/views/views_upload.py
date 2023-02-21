# from django.shortcuts import render, redirect
from django.core.serializers import serialize
# data = serializers.serialize("xml", SomeModel.objects.all())

from ..models import Cadastro,Referencia
import json
from django.http import JsonResponse,HttpResponse

def dados_cadastro_json(request):
    data_json = []
    data_json.append(list(Cadastro.objects.values()))
    data_json.append(list(Referencia.objects.values()))

    return JsonResponse(data_json, safe=False)



# from django.views.generic import TemplateView
# from django.contrib import messages

# from ..forms import FormUploadDados

# import os, json
# from django.conf import settings

# #@method_decorator(login_required, name='dispatch')
# class EnviarDados(TemplateView):
#     form_upload = FormUploadDados
#     template_name = "modelos/formulario_beneficios.html"
#     context = {'titulo_pagina': "Enviar ",'link':'/'}
#     def get(self, request, *args, **kwargs):
#         forms_generic = {"Dados": self.form_upload()}
#         self.context['forms_generic'] = forms_generic
#         return render(request, self.template_name, self.context)

#     def post(self, request, *args, **kwargs):
        
#         form = self.form_upload(request.POST,request.FILES)
#         forms_generic = {"Informações da Solicitação": form}
    
#         if form.is_valid():
#             pasta_temporaria = os.path.join(settings.BASE_DIR, "media/")
#             arquivo = form.cleaned_data['arquivo_dados']
#             nome_arquivo = str(form.cleaned_data['arquivo_dados'])
#             tipo = form.cleaned_data['tipo_informacoes']
#             tecnico = get_object_or_404(Tecnico,usuario=request.user) #.objects.get()
#             print(tecnico.cargo)
#             with open(f'{pasta_temporaria}{nome_arquivo}', 'wb+') as destination:
#                 for chunk in arquivo.chunks():
#                     destination.write(chunk)
#             caminho_arquivo = os.path.join(pasta_temporaria, nome_arquivo)
#             with open(caminho_arquivo, encoding='utf-8') as meu_json:
#                 dados = json.load(meu_json)
#             if tipo == "1":
#                 for dado in dados:
#                     # print(dado['nome'])
#                     try:
#                         Bairro.objects.create(nome=dado['nome'])
#                     except:
#                         pass
#             else:
#                 for dado in dados:
#                     print(tecnico)
#                     # salvar_cadastros_massivo(dado, tecnico)
#             #return redirect('avaliar_solicitacao',registro.id)
#             os.remove(caminho_arquivo)
            
#         self.context['forms_generic'] = forms_generic
#         return render(request, self.template_name, self.context)
 
