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
	data_nascimento=data_nascimento, cpf=cpf, nis=nis, trabalho=trabalho, escolaridade=escolaridade,
	contato=contato, renda=renda, parentesco=parentesco, cadastro_membro=cadastro)

def editar_membro(membro_bd, form):
	membro_bd.nome = form.cleaned_data['nome'] if form.cleaned_data['nome'] else membro_bd.nome
	# membro_bd.situacao_civil =  form.cleaned_data['situacao_civil']
	membro_bd.sexo = form.cleaned_data['sexo']
	membro_bd.data_nascimento = form.cleaned_data['data_nascimento']
	membro_bd.cpf = form.cleaned_data['cpf'] if form.cleaned_data['cpf'] else membro_bd.cpf
	membro_bd.nis = form.cleaned_data['nis'] if form.cleaned_data['nis'] else membro_bd.nis
	membro_bd.escolaridade = form.cleaned_data['escolaridade']
	membro_bd.contato = form.cleaned_data['contato']
	# membro_bd.contato2 = form.cleaned_data['contato2']
	membro_bd.trabalho = form.cleaned_data['trabalho']
	membro_bd.renda = form.cleaned_data['renda']
	membro_bd.parentesco = form.cleaned_data['parentesco']
	membro_bd.save(force_update=True)
	return membro_bd

def editar_pessoa(pessoa_bd, form):
	has_change = False
	lista_alteracoes = []
	if pessoa_bd.nome != form.cleaned_data['nome'] and form.cleaned_data['nome']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('nome').verbose_name,
												valor_antigo=pessoa_bd.nome if pessoa_bd.nome else "-",
												valor_novo=form.cleaned_data['nome']))
		pessoa_bd.nome = form.cleaned_data['nome']
		has_change = True

	if pessoa_bd.apelido != form.cleaned_data['apelido']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('apelido').verbose_name,
												valor_antigo=pessoa_bd.apelido if pessoa_bd.apelido else "-",
												valor_novo=form.cleaned_data['apelido']))
		pessoa_bd.apelido = form.cleaned_data['apelido']
		has_change = True

	if pessoa_bd.nome_social != form.cleaned_data['nome_social']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('nome_social').verbose_name,
												valor_antigo=pessoa_bd.nome_social if pessoa_bd.nome_social else "-",
												valor_novo=form.cleaned_data['nome_social']))
		pessoa_bd.nome_social = form.cleaned_data['nome_social']
		has_change = True

	if pessoa_bd.situacao_civil != form.cleaned_data['situacao_civil']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('situacao_civil').verbose_name,
												valor_antigo=pessoa_bd.situacao_civil if pessoa_bd.situacao_civil else "-",
												valor_novo=form.cleaned_data['situacao_civil']))
		pessoa_bd.situacao_civil = form.cleaned_data['situacao_civil']
		has_change = True

	if pessoa_bd.identidade_genero != form.cleaned_data['identidade_genero']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('identidade_genero').verbose_name,
												valor_antigo=pessoa_bd.identidade_genero if pessoa_bd.identidade_genero else "-",
												valor_novo=form.cleaned_data['identidade_genero']))
		pessoa_bd.identidade_genero = form.cleaned_data['identidade_genero']
		has_change = True

	if pessoa_bd.cor_raca != form.cleaned_data['cor_raca']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('cor_raca').verbose_name,
												valor_antigo=pessoa_bd.cor_raca,
												valor_novo=form.cleaned_data['cor_raca']))
		pessoa_bd.cor_raca = form.cleaned_data['cor_raca']
		has_change = True

	if pessoa_bd.sexo != form.cleaned_data['sexo']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('sexo').verbose_name,
												valor_antigo=pessoa_bd.sexo,
												valor_novo=form.cleaned_data['sexo']))
		pessoa_bd.sexo = form.cleaned_data['sexo']
		has_change = True

	if pessoa_bd.data_nascimento != form.cleaned_data['data_nascimento']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('data_nascimento').verbose_name,
												valor_antigo=pessoa_bd.data_nascimento,
												valor_novo=form.cleaned_data['data_nascimento']))
		pessoa_bd.data_nascimento = form.cleaned_data['data_nascimento']
		has_change = True

	if pessoa_bd.cpf != form.cleaned_data['cpf'] and form.cleaned_data['cpf']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('cpf').verbose_name,
												valor_antigo=pessoa_bd.cpf,
												valor_novo=form.cleaned_data['cpf']))
		pessoa_bd.cpf = form.cleaned_data['cpf']
		has_change = True

	if pessoa_bd.nis != form.cleaned_data['nis'] and form.cleaned_data['nis']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('nis').verbose_name,
												valor_antigo=pessoa_bd.nis,
												valor_novo=form.cleaned_data['nis']))
		pessoa_bd.nis = form.cleaned_data['nis']
		has_change = True

	if pessoa_bd.escolaridade != form.cleaned_data['escolaridade']:
		dict_data = dict(form.fields['escolaridade']._choices)
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('escolaridade').verbose_name,
												valor_antigo=pessoa_bd.get_escolaridade_display(),
												valor_novo=dict_data[form.cleaned_data['escolaridade']]))
		pessoa_bd.escolaridade = form.cleaned_data['escolaridade']
		has_change = True

	if pessoa_bd.contato != form.cleaned_data['contato']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('contato').verbose_name,
												valor_antigo=pessoa_bd.contato,
												valor_novo=form.cleaned_data['contato']))
		pessoa_bd.contato = form.cleaned_data['contato']
		has_change = True

	if pessoa_bd.contato2 != form.cleaned_data['contato2']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('contato2').verbose_name,
													valor_antigo=pessoa_bd.contato2,
													valor_novo=form.cleaned_data['contato2']))
		pessoa_bd.contato2 = form.cleaned_data['contato2']
		has_change = True

	if pessoa_bd.renda != form.cleaned_data['renda']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('renda').verbose_name,
												valor_antigo=pessoa_bd.renda,
												valor_novo=form.cleaned_data['renda']))
		pessoa_bd.renda = form.cleaned_data['renda']
		has_change = True
	if pessoa_bd.cadastro_unico != form.cleaned_data['cadastro_unico']:
		dict_data = dict(form.fields['cadastro_unico']._choices)
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('cadastro_unico').verbose_name,
												valor_antigo=pessoa_bd.get_cadastro_unico_display(),
												valor_novo=dict_data[form.cleaned_data['cadastro_unico']]))

		pessoa_bd.cadastro_unico = form.cleaned_data['cadastro_unico']
		has_change = True

	if pessoa_bd.trabalho != form.cleaned_data['trabalho']:
		lista_alteracoes.append(ChangeCampoData(campo=pessoa_bd._meta.get_field('trabalho').verbose_name,
												valor_antigo=pessoa_bd.trabalho,
												valor_novo=form.cleaned_data['trabalho']))
		pessoa_bd.trabalho = form.cleaned_data['trabalho']
		has_change = True

	if has_change:
		pessoa_bd.save(force_update=True)
	return has_change, lista_alteracoes


def editar_endereco(endereco, form):
	has_change = False
	lista_alteracoes = []
	if endereco.logradouro != form.cleaned_data['logradouro']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('logradouro').verbose_name,
													valor_antigo=endereco.logradouro if endereco.logradouro else "-", valor_novo=form.cleaned_data['logradouro']))
		endereco.logradouro = form.cleaned_data['logradouro']
		has_change = True

	if endereco.numero != form.cleaned_data['numero']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('numero').verbose_name,
												valor_antigo=endereco.numero if endereco.numero else "-",
												valor_novo=form.cleaned_data['numero']))
		endereco.numero = form.cleaned_data['numero']
		has_change = True

	if endereco.complemento != form.cleaned_data['complemento']:
		lista_alteracoes.append(ChangeCampoData(campo=endereco._meta.get_field('complemento').verbose_name,
												valor_antigo=endereco.complemento if endereco.complemento else "-",
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