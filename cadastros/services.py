from .models import *

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


def editar_endereco(endereco,form):
	endereco.logradouro = form.cleaned_data['logradouro']
	endereco.numero = form.cleaned_data['numero']
	endereco.complemento = form.cleaned_data['complemento']
	endereco.bairro = form.cleaned_data['bairro']
	endereco.save()
	return endereco


def buscar_cadastro_nome(nome):
	pessoas = Pessoa.objects.all()
	cadastros_bd = Cadastro.objects.all()
	lista_encontrados =[]
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
	print(len(pessoas))
	cadastros_bd = Cadastro.objects.all()
	lista_cadastros = []
	for pessoa in pessoas:
		print(pessoa)
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
						# lista_cadastros.append(cadastros_bd.get(id=membro.cadastro_membro.id))
	print(lista_cadastros)
	return lista_cadastros

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


def buscar_cadastro_bairro(bairro):
	# bairro_bd = Bairro.objects.filter(nome=bairro)
	cadastros = Cadastro.objects.filter(endereco__bairro__nome=bairro).all()
	lista_cadastros = []
	for cadastro in cadastros:
		if cadastro not in lista_cadastros:
			lista_cadastros.append(cadastro)
		
	return lista_cadastros



if __name__ =="__main__":
    pass