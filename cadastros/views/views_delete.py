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
class DeleteMembroView(TemplateView):
    template_name = "cadastros/geral/dados_excluir.html"
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
        self.context['dados_cadastro'] = cadastro
        self.context['dados_membro'] = MembroDados(membro)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pk = self.get_pk()
        membro = get_object_or_404(Membros, id=pk)
        cadastro = get_object_or_404(Cadastro, id=membro.cadastro_membro.id)

        self.context['id_cancelar'] = f'id:{cadastro.id}'
        self.context['dados_cadastro'] = cadastro
        self.context['dados_membro'] = MembroDados(membro)
        # print(request.POST)
        if "confirmar" in request.POST:
            membro.delete()
            messages.success(request, f'Informações do Membro Foram Excluídas!')
            return redirect('listar_cadastros', f'id:{cadastro.id}')
        return render(request, self.template_name, self.context)

    def get_pk(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return self.kwargs['pk']
        else:
            redirect('listar_cadastros')


