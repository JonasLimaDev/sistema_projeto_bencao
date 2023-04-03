# from .filters import total_cadastro_bairro, total_cadastro_ruc, total_cadastro_cras
from .filters import *
from pprint import pprint

from django.conf import settings

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Image, Table, TableStyle
# from functools import partial
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

import io,os
def set_fonts():
    """Função para carregar a fonte Arial para poder usar nos documentos"""
    lista_fontes = [
        "fonts/arial.ttf",
        "fonts/arial-bold.ttf",
        "fonts/arial-italic.ttf",
        "fonts/arial-bold-italic.ttf"
    ]
    lista_fontes2 = [
        "fonts\\arial.ttf",
        "fonts\\arial-bold.ttf",
        "fonts\\arial-italic.ttf",
        "fonts\\arial-bold-italic.ttf"
    ]
    path = os.path.join(settings.STATIC_ROOT, lista_fontes[0])
    try:
        pdfmetrics.registerFont(TTFont('Arial', str(path)))
    except:
        pdfmetrics.registerFont(TTFont('Arial', str(path).replace('/', '\\')))
    path = os.path.join(settings.STATIC_ROOT, lista_fontes[1])
    try:
        pdfmetrics.registerFont(TTFont('ArialN', str(path)))
    except:
        pdfmetrics.registerFont(TTFont('ArialN',  str(path).replace('/', '\\')))

    path = os.path.join(settings.STATIC_ROOT, lista_fontes[2])
    try:
        pdfmetrics.registerFont(TTFont('ArialI',  str(path)))
    except:
        # path = os.path.join(settings.STATIC_ROOT, lista_fontes2[2])
        pdfmetrics.registerFont(TTFont('ArialI',  str(path).replace('/', '\\')))

    path = os.path.join(settings.STATIC_ROOT, lista_fontes[3])
    try:
        pdfmetrics.registerFont(TTFont('ArialNI',  str(path)))
    except:
        # path = os.path.join(settings.STATIC_ROOT, lista_fontes2[3])
        pdfmetrics.registerFont(TTFont('ArialNI',  str(path).replace('/', '\\')))

    registerFontFamily('Arial', normal='ArialR', bold='ArialN', italic='ArialI', boldItalic='ArialNI')


def header_footer(canvas, doc):
    styles = getSampleStyleSheet()
    styleF = ParagraphStyle('rodape',

                           fontSize=10,
                           parent=styles['Normal'],
                           alignment=1,
                           spaceAfter=14)
    canvas.saveState()
    local = "img/timbre.jpg"
    path = os.path.join(settings.STATIC_ROOT, local)
    # print(path)
    # open(local,'rb')
    # logo = "logos.png"
    # print(logo)
    im = Image(path, 10*cm,1.5*cm)


    # Header
    imagem =  im

    w, h = imagem.wrap(doc.width, doc.topMargin)
    imagem.drawOn(canvas, doc.leftMargin+doc.rightMargin, doc.height + doc.topMargin -h/2)
    # header =  Paragraph('Prefeitura Municipal de Altamira<br/>Secretaria Municipal de Assistência e Promoção Social<br/>Projeto Galileu', styleHeader)

    # w, h = header.wrap(doc.width, doc.topMargin)
    # header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h/2)


    # Footer
    footer = Paragraph('Rua Acesso Dois, 370 - Esplanada do Xingu - Telefone: (93) 3515-2416<br/>CEP 68372-855 Altamira/PA -  assistenciasocial.atm.gab@gmail.com', styleF)
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - h)
    # Release the canvas
    canvas.restoreState()


def gerar_doc(text_param):
    """Função que constroi o documento em pdf.
    Recebe uma lista com os parágrafos para adicionar no documento.
    Retorna os Bytes para renderizar o documento."""

    # cria os bytes pra receber os dados do documento
    buffer = io.BytesIO()

    TopMargin = 2 * cm
    #Cria a instância do documento
    doc = BaseDocTemplate(buffer, author="Web System", title="TERMO LOTE")

    # definição das margens
    frame = Frame(2.5*cm, 1*cm, doc.width+1.5*cm, doc.height+3.5*cm)

    template = PageTemplate(id='termo_entrega_orgão', frames=frame,)

    doc.addPageTemplates([template])
    text = []
    doc = BaseDocTemplate(buffer,author="Sistema Projeto Bênção", title="Dados do Sistema", topMargin=TopMargin)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-2*cm, id='normal')
    template = PageTemplate(id='dados', frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])

    #insere a imagem no documento
    # text.append(img)

    #constroi o documento passando a lista de base e a lista de parágarfos do parâmetro
    doc.build(text+text_param)

    buffer.seek(0)
    return buffer


def printer_total_bairro():
    dados_bairros = total_cadastro_bairro()

    # ---- Adiciona os parágrafos do documento em uma lista
    counter = 0
    # -------- Organiza os dados em listas para criar a tabela
    data = [["Bairro","Quantidade","","Bairro","Quantidade"]]
    for chave, valor in dados_bairros.items():
        if counter == 0:
            linha = []
        linha.append(chave)
        linha.append(valor)
        counter += 1
        if counter < 2:
            linha.append("")
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


def printer_referecias():
    dados = buscar_cadastro()
    styles = getSampleStyleSheet()
    styleNormal = ParagraphStyle('corpo_normal', fontFamily="Arial", fontSize=12,
                                 parent=styles['Normal'], alignment=0, leading=18, spaceBefore=0, spaceAfter=0)

    lista = [["Ord.", "Nome", "Bairro", "Endereco", "Telefone"]]
    contador = 1

    for cadastro in dados:
        endereco = f"{cadastro.endereco.logradouro}, Nº {cadastro.endereco.numero}"
        lista.append([Paragraph(str(contador), styleNormal),
                      Paragraph(str(cadastro.responsavel_familiar), styleNormal),
                      Paragraph(str(cadastro.endereco.bairro), styleNormal),
                      Paragraph(endereco,  styleNormal),
                      Paragraph(str(cadastro.responsavel_familiar.contato if cadastro.responsavel_familiar.contato else '--------' ), styleNormal)])
        contador += 1
    return lista


def printer_ficha(id):
    cadastro = buscar_cadastro(id)
    styles = getSampleStyleSheet()
    styleNormal = ParagraphStyle('corpo_normal', fontFamily="Arial", fontSize=12,
                                 parent=styles['Normal'], alignment=0, leading=12, spaceBefore=0, spaceAfter=0)
    p_nome = Paragraph(str(cadastro.responsavel.nome), styleNormal)
    p_apelido = Paragraph(str(cadastro.responsavel.apelido), styleNormal)
    p_sexo = Paragraph(str(cadastro.responsavel.sexo), styleNormal)
    p_genero = Paragraph(str(cadastro.responsavel.nome), styleNormal)
    p_nome_social = Paragraph(str(cadastro.responsavel.nome), styleNormal)
    p_situacao_civil = Paragraph(str(cadastro.responsavel.nome), styleNormal)
    p_data_nascimento= Paragraph(str(cadastro.responsavel.nome), styleNormal)
    p_idade =  Paragraph(str(cadastro.responsavel.idade), styleNormal)
    linhas = [
        [
            Paragraph("<b>Nome:</b>",styleNormal), p_nome, "", "", Paragraph("<b>Apelido:</b>", styleNormal), p_apelido
        ],        
        [
            Paragraph("<b>Sexo:</b>",styleNormal), p_sexo,
            Paragraph("<b>Identidade de Gênero:</b>",styleNormal), cadastro.responsavel.identidade_genero,
            Paragraph("<b>Nome Social:</b>",styleNormal), cadastro.responsavel.nome_social
        ],
        [
        Paragraph("<b>Situação Civil:</b>",styleNormal), cadastro.responsavel.situacao_civil,
        Paragraph("<b>Data de Nascimento:</b>",styleNormal),
        cadastro.responsavel.data_nascimento.strftime("%d/%m/%Y") if cadastro.responsavel.data_nascimento else "-" ,
        Paragraph("<b>Idade:</b>",styleNormal), p_idade ],
        
        ]
    # linhas[0][1] = 
    
    return linhas