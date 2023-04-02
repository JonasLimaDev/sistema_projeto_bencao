from .filters import total_cadastro_bairro, total_cadastro_ruc, total_cadastro_cras
from pprint import pprint

import io, os
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

def set_fonts():
    """Função para carregar a fonte Arial para poder usar nos documentos"""
    arial_normal = "fonts/arial.ttf"

    path = os.path.join(settings.STATIC_ROOT, arial_normal)
    pdfmetrics.registerFont(TTFont('Arial', path))

    arial_negrito = "fonts/arial-bold.ttf"
    path = os.path.join(settings.STATIC_ROOT, arial_negrito)
    pdfmetrics.registerFont(TTFont('ArialN', path))

    arial_italico = "fonts/arial-italic.ttf"
    path = os.path.join(settings.STATIC_ROOT, arial_italico)
    pdfmetrics.registerFont(TTFont('ArialI', path))

    arial_italico_negrito = "fonts/arial-bold-italic.ttf"
    path = os.path.join(settings.STATIC_ROOT, arial_italico_negrito)
    pdfmetrics.registerFont(TTFont('ArialNI', path))

    registerFontFamily('Arial', normal='ArialR', bold='ArialN', italic='ArialI', boldItalic='ArialNI')

def printer_total_bairro():
    dados_bairros = total_cadastro_bairro()

    # ---- Adiciona os parágrafos do documento em uma lista
    counter = 0
    # -------- Organiza os dados em listas para criar a tabela
    data = [["Bairro","Quantidade","","Bairro","Quantidade",""]]
    for chave, valor in dados_bairros.items():
        if counter == 0:
            linha = []
        linha.append(chave)
        linha.append(valor)
        linha.append("")
        counter += 1
        if counter == 2:
            data.append(linha)
            counter = 0

    return data


def printer_total_ruc():
    dados = total_cadastro_ruc()
    lista = [["RUC","Quantidade"]]
    for chave, valor in dados.items():
        lista.append([chave, valor])

    return lista

def printer_total_cras():
    dados = total_cadastro_cras()
    lista = [["CRAS","Quantidade"]]
    for chave, valor in dados.items():
        lista.append([chave, valor])

    return lista