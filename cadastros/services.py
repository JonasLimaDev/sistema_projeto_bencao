from .models import *
import re
from change_control.classes_change_control import ChangeCampoData

def salvar_membro(form,cadastro):
	nome = form.cleaned_data['nome']
	# print(nome) 
	# situacao_civil =  form.cleaned_data['situacao_civil']
	sexo = form.cleaned_data['sexo']
	data_nascimento = form.cleaned_data['data_nascimento']
	cpf = form.cleaned_data['cpf']
	nis = form.cleaned_data['nis']
	escolaridade = form.cleaned_data['escolaridade']
	contato = form.cleaned_data['contato']
	# contato2 = form.cleaned_data['contato2']
	trabalho = form.cleaned_data['trabalho']
	renda = form.cleaned_data['renda']
	parentesco = form.cleaned_data['parentesco']
	Membros.objects.create(nome=nome, sexo=sexo,
	data_nascimento=data_nascimento,cpf=cpf,nis=nis,trabalho=trabalho,escolaridade=escolaridade,
	contato=contato,
	renda=renda,parentesco=parentesco,cadastro_membro=cadastro)

def editar_membro(membro_bd,form):
	membro_bd.nome = form.cleaned_data['nome'] if form.cleaned_data['nome'] else membro_bd.nome
	# membro_bd.situacao_civil =  form.cleaned_data['situacao_civil']
	membro_bd.sexo = form.cleaned_data['sexo']
	membro_bd.data_nascimento = form.cleaned_data['data_nascimento']
	membro_bd.cpf = form.cleaned_data['cpf']  if form.cleaned_data['cpf'] else membro_bd.cpf
	membro_bd.nis = form.cleaned_data['nis']  if form.cleaned_data['nis'] else membro_bd.nis
	membro_bd.escolaridade = form.cleaned_data['escolaridade']
	membro_bd.contato = form.cleaned_data['contato']
	# membro_bd.contato2 = form.cleaned_data['contato2']
	membro_bd.trabalho = form.cleaned_data['trabalho']
	membro_bd.renda = form.cleaned_data['renda']
	membro_bd.parentesco = form.cleaned_data['parentesco']
	membro_bd.save(force_update=True)
	return membro_bd

def editar_pessoa(pessoa_bd, form):
	pessoa_bd.nome = form.cleaned_data['nome'] if form.cleaned_data['nome'] else pessoa_bd.nome
	pessoa_bd.apelido = form.cleaned_data['apelido'] if form.cleaned_data['apelido'] else pessoa_bd.apelido
	pessoa_bd.nome_social= form.cleaned_data['nome_social'] if form.cleaned_data['nome_social'] else pessoa_bd.nome_social
	pessoa_bd.situacao_civil =  form.cleaned_data['situacao_civil']
	pessoa_bd.identidade_genero =  form.cleaned_data['identidade_genero']
	pessoa_bd.cor_raca =  form.cleaned_data['cor_raca']
	
	pessoa_bd.sexo = form.cleaned_data['sexo']
	pessoa_bd.data_nascimento = form.cleaned_data['data_nascimento']
	pessoa_bd.cpf = form.cleaned_data['cpf']  if form.cleaned_data['cpf'] else pessoa_bd.cpf
	pessoa_bd.nis = form.cleaned_data['nis']  if form.cleaned_data['nis'] else pessoa_bd.nis
	pessoa_bd.escolaridade = form.cleaned_data['escolaridade']
	pessoa_bd.contato = form.cleaned_data['contato']
	pessoa_bd.renda = form.cleaned_data['renda']
	pessoa_bd.save(force_update=True)
	return pessoa_bd


def editar_endereco(endereco, form):
	has_change = False
	lista_alteracoes = []
	if endereco.logradouro != form.cleaned_data['logradouro']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('logradouro').verbose_name,
													valor_antigo=endereco.logradouro, valor_novo=form.cleaned_data['logradouro']))
		endereco.logradouro = form.cleaned_data['logradouro']
		has_change = True

	if endereco.numero != form.cleaned_data['numero']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('numero').verbose_name,
												valor_antigo=endereco.numero,
												valor_novo=form.cleaned_data['numero']))
		endereco.numero = form.cleaned_data['numero']
		has_change = True

	if endereco.complemento != form.cleaned_data['complemento']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('complemento').verbose_name,
												valor_antigo=endereco.complemento,
												valor_novo=form.cleaned_data['complemento']))
		endereco.complemento = form.cleaned_data['complemento']
		has_change = True

	if endereco.ruc != form.cleaned_data['ruc']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('ruc').verbose_name,
												valor_antigo=endereco.ruc,
												valor_novo=form.cleaned_data['ruc']))
		endereco.ruc = form.cleaned_data['ruc']
		has_change = True

	if endereco.bairro != form.cleaned_data['bairro']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('bairro').verbose_name,
												valor_antigo=endereco.bairro,
												valor_novo=form.cleaned_data['bairro']))
		endereco.bairro = form.cleaned_data['bairro']
		has_change = True
	if has_change:
		endereco.save()

	return has_change, lista_alteracoes



def inserir_bairros():
	nomes = """
	Alberto Soares
	Aparecida
	Ayrton Senna I
	Ayrton Senna II
	Bela Vista
	Boa Esperança
	Boa Sorte
	Bonanza
	Brasília
	Centro
	Colina
	Esplanada do Xingu
	Ibiza
	Jardim Altamira
	Jardim França
	Jardim Independente I
	Jardim Independente II
	Jardim Primavera
	Jardim Uirapuru
	Lama Negra
	Liberdade
	Mexicano
	Mutirão
	Nova Altamira
	Paixão de Cristo
	Parque Ipê
	Premem
	Santa Ana
	Santa Benedita
	São Francisco
	São Sebastião
	Sudam I
	Sudam II
	Viena
	Zona Rural
	"""
	lista_bairros = nomes.split('\n')
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




def is_cpf(cpf):
	expressao = re.compile('\d{3}\.\d{3}\.\d{3}\-\d{2}')
	if expressao.search(cpf):
		return True
	else:
		return False

if __name__ =="__main__":
    pass