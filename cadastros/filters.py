from .models import *
import re
from .entidades.dados import CadastroData

def buscar_cadastro_nome(nome):
    pessoas = Pessoa.objects.all()
    cadastros_bd = Cadastro.objects.all()
    lista_encontrados = []
    lista_cadastros = []
    for pessoa in pessoas:
        if nome.lower() in pessoa.nome.lower():
            lista_encontrados.append(pessoa)
    if lista_encontrados:
        for pessoa in lista_encontrados:
            cadastros = cadastros_bd.filter(responsavel_familiar=pessoa)
            if cadastros:
                for cadastro in cadastros:
                    if cadastro not in lista_cadastros:
                        lista_cadastros.append(cadastro)
            else:
                membros = Membros.objects.filter(id=pessoa.id)
                if membros:
                    for membro in membros:
                        cadastro = cadastros_bd.get(id=membro.cadastro_membro.id)
                        if cadastro not in lista_cadastros:
                            lista_cadastros.append(cadastro)
    return lista_cadastros


def buscar_cadastro_cpf(cpf):
    pessoas = Pessoa.objects.filter(cpf__exact=cpf)
    # print(len(pessoas))
    cadastros_bd = Cadastro.objects.all()
    lista_cadastros = []
    for pessoa in pessoas:
        cadastros = cadastros_bd.filter(responsavel_familiar=pessoa)
        for cadastro in cadastros:
            if cadastro not in lista_cadastros:
                lista_cadastros.append(cadastro)
            else:
                membros = Membros.objects.filter(id=pessoa.id)
                if membros:
                    for membro in membros:
                        cadastro = cadastros_bd.get(id=membro.cadastro_membro.id)
                        if cadastro not in lista_cadastros:
                            lista_cadastros.append(cadastro)
    return lista_cadastros


def buscar_cadastro_bairro(bairro):
    # bairro_bd = Bairro.objects.filter(nome=bairro)
    cadastros = Cadastro.objects.filter(endereco__bairro__nome=bairro).all()
    lista_cadastros = []
    for cadastro in cadastros:
        if cadastro not in lista_cadastros:
            lista_cadastros.append(cadastro)
    return lista_cadastros


def total_cadastro_bairro():
    # bairro_bd = Bairro.objects.filter(nome=bairro)
    dados = {}
    for bairro in Bairro.objects.all():
        cadastros = Cadastro.objects.filter(endereco__bairro__nome=bairro).all()
        dados[bairro] = len(cadastros)
    # print(dados)
    return dados


def total_cadastro_ruc():
    # bairro_bd = Bairro.objects.filter(nome=bairro)
    RUCs = {'1': 'Nenhum',
            '2': 'Água Azul',
            '3': 'Jatobá',
            '4': 'São Joaquim',
            '5': 'Casa Nova',
            '6': 'Laranjeiras',
            }

    dados = {}
    for codigo, ruc in RUCs.items():
        cadastros = Cadastro.objects.filter(endereco__ruc=codigo).all()
        dados[ruc] = len(cadastros)

    return dados


def total_cadastro_cras():
    # bairro_bd = Bairro.objects.filter(nome=bairro)
    CRAS = {
        '1': 'CRAS I',
        '2': 'CRAS II',
        '3': 'CRAS III',
    }

    dados = {}
    for codigo, cras in CRAS.items():
        cadastros = Cadastro.objects.filter(abrangencia=codigo).all()
        dados[cras] = len(cadastros)

    return dados


def buscar_cadastro_ruc(bairro):
    # bairro_bd = Bairro.objects.filter(nome=bairro)
    cadastros = Cadastro.objects.filter(endereco__ruc=bairro).all()
    lista_cadastros = []
    for cadastro in cadastros:
        if cadastro not in lista_cadastros:
            lista_cadastros.append(cadastro)

    return lista_cadastros


def buscar_cadastro(filter=None):
    # bairro_bd = Bairro.objects.filter(nome=bairro)
    if filter:
        cadastro = Cadastro.objects.get(id=filter)
        return CadastroData(cadastro)

    else:
        cadastros = Cadastro.objects.select_related().all()

    return cadastros
