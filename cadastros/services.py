from .models import *
import re
from change_control.classes_change_control import ChangeCampoData



from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from django.conf import settings

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph,Image,Table, TableStyle
# from functools import partial
from reportlab.lib.units import inch, cm
import io,os
from django.conf import settings
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


def salvar_membro(form,cadastro):
	nome = form.cleaned_data['nome']
	sexo = form.cleaned_data['sexo']
	data_nascimento = form.cleaned_data['data_nascimento']
	cpf = form.cleaned_data['cpf']
	nis = form.cleaned_data['nis']
	escolaridade = form.cleaned_data['escolaridade']
	contato = form.cleaned_data['contato']
	trabalho = form.cleaned_data['trabalho']
	renda = form.cleaned_data['renda']
	parentesco = form.cleaned_data['parentesco']
	Membros.objects.create(nome=nome, sexo=sexo,
	data_nascimento=data_nascimento, cpf=cpf, nis=nis, trabalho=trabalho, escolaridade=escolaridade,
	contato=contato, renda=renda, parentesco=parentesco, cadastro_membro=cadastro)


def inserir_bairros():
	nomes = """
		Alberto Soares|Aparecida|Ayrton Senna I|Ayrton Senna II|Bela Vista|Boa Esperança|Boa Sorte|
		Bonanza|Brasília|Centro|Colina|Esplanada do Xingu|Ibiza|Jardim Altamira|Jardim França|Jardim Independente I|
		Jardim Independente II|Jardim Primavera|Jardim Uirapuru|Lama Negra|Liberdade|Mexicano|Mutirão|Nova Altamira|
		Paixão de Cristo|Parque Ipê|Premem|Santa Ana|Santa Benedita|São Francisco|São Sebastião|Sudam I|Sudam II|
		Viena|Zona Rural|
	"""

	lista_bairros = nomes.replace("\n", "").split('|')
	for bairro in lista_bairros:
		if bairro[1:] != '':
			try:
				Bairro.objects.create(nome=bairro[1:])
			except:
				print(f'Bairro {bairro[1:]} já existe')


def salvar_cadastros_massivo(dados,tecnico):

	situacao_habitacao = Habitacao.objects.create(situacao_moradia="1", numero_moradores=2, numero_comodos=3)

	bairro, criado = Bairro.objects.get_or_create(nome=dados['bairro'])

	responsavel_familiar = Pessoa.objects.create(nome=dados['nome'],situacao_civil="1",
						sexo=dados['sexo'],data_nascimento=dados['data_nascimento'],cpf=dados['cpf'],nis="",
												 escolaridade="1",contato=dados['celular'],renda=400)

	endereco = Endereco.objects.create(logradouro=dados['endereco'],numero=dados['numero'],bairro=bairro)
	Cadastro.objects.create(situacao_habitacao=situacao_habitacao,responsavel_familiar=responsavel_familiar,
							responsavel_cadastro=tecnico,endereco=endereco)

def lista_objeto_str(lista):
	conjunto_str=""
	for item in lista:
		conjunto_str += f"{item}, "
	conjunto_str = conjunto_str[:-2]
	return conjunto_str

def editar_model_data(inst_model,inst_form,ignore=[]):
	"""Função para edição da tabela de dados habitacionais"""
	has_change = False # Variável pra identificar se houve alteração
	lista_alteracoes = [] # lista com a classe de alterações
	inst_model_data = vars(inst_model) # variáveis da tabela de habitação
	
	for field in inst_form:
		"""Percore todos os campos do formulário"""
		if inst_model._meta.get_field(field.name).is_relation and field.name not in ignore:
			""" Verifica se o campo possui alguma relação"""
			valor_atual = inst_form.fields[field.name]._queryset.get(id=inst_model_data[f"{field.name}_id"])
			valor_form = inst_form.cleaned_data[field.name]
			if valor_atual != valor_form:
				lista_alteracoes.append(ChangeCampoData(campo=inst_model._meta.get_field(field.name).verbose_name,
												valor_antigo=valor_atual  if valor_atual  else "-",
												valor_novo=valor_form))
				setattr(inst_model, f"{field.name}_id", valor_form.id)
				has_change = True
		elif field.name not in ignore and  inst_model_data[field.name] != inst_form.cleaned_data[field.name]:
			if hasattr(inst_form.fields[field.name], "_choices"):
				"""Verifica se o Campo e do tipo CHOICES"""	
				dict_data_form = dict(inst_form.fields[field.name]._choices) # gera o dicionário de valores e alternativas do choices

				lista_alteracoes.append(ChangeCampoData(campo=inst_model._meta.get_field(field.name).verbose_name,
												valor_antigo=dict_data_form[inst_model_data[field.name]],
												valor_novo=dict_data_form[inst_form.cleaned_data[field.name]])
										) # Adiciona o objeto de alteração para a lista
			else:
				lista_alteracoes.append(ChangeCampoData(campo=inst_model._meta.get_field(field.name).verbose_name,
												valor_antigo=inst_model_data[field.name] if inst_model_data[field.name] else "-",
												valor_novo=inst_form.cleaned_data[field.name])
										) # Adiciona o objeto de alteração para a lista
			
			setattr(inst_model, field.name, inst_form.cleaned_data[field.name]) # altera os valores na instancia de modelo do banco de dados
			has_change = True # indica que houve uma alteração


		
		if has_change:
			"""Verifica se houve alteração e salva o model"""
			inst_model.save()
	return has_change, lista_alteracoes
	


def is_cpf(cpf):
	expressao = re.compile('\d{3}\.\d{3}\.\d{3}\-\d{2}')
	if expressao.search(cpf):
		return True
	else:
		return False


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
if __name__ =="__main__":
    pass