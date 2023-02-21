from .models import Pessoa


def gerar_digito(sequencia,peso_inicial):
    soma = 0
    digito_verificador = 0
    for digito in sequencia:
        soma += int(digito)*peso_inicial
        peso_inicial+=1
    if soma % 11 != 10:
        digito_verificador = soma % 11
    return str(digito_verificador)


def validar_cpf(cpf,lista_erros,NEW=True):
    if len(cpf) > 11:
        lista_erros['cpf'] = "Formato de CPF Inválido! digite apenas os Números"
    elif len(cpf) == 11:
        if not cpf.isdigit():
            lista_erros['cpf'] = "CPF inválido digite apenas os NÚMEROS"
        else:
            digitos_cpf = cpf[9:11]
            digito_verificador1 = gerar_digito(cpf[0:9], 1)
            sequencia = cpf[0:9]+digito_verificador1 
            digito_verificador2 = gerar_digito(sequencia, 0)
            resultado = digito_verificador1+digito_verificador2
            if digitos_cpf != resultado:
                lista_erros['cpf'] = "CPF inválido verifique os dígitos e tente novamente"
            elif NEW:
                pessoa = Pessoa.objects.filter(cpf=cpf)
                if pessoa:
                    lista_erros['cpf'] = "Este CPF Já está Registrado"
    else:
        lista_erros['cpf'] = "CPF incompleto informe todos os 11 dígitos"


def validar_cpf_edicao(cpf,lista_erros):
    if len(cpf) > 11:
        lista_erros['cpf'] = "Formato de CPF Inválido! digite apenas os Números"
    elif len(cpf) == 11:
        if not cpf.isdigit():
            lista_erros['cpf'] = "CPF inválido digite apenas os NÚMEROS"
        else:
            digitos_cpf = cpf[9:11]
            digito_verificador1 = gerar_digito(cpf[0:9],1)
            sequencia = cpf[0:9]+digito_verificador1 
            digito_verificador2 = gerar_digito(sequencia,0)
            resultado = digito_verificador1+digito_verificador2
            if digitos_cpf != resultado:
                lista_erros['cpf'] = "CPF inválido verifique os dígitos e tente novamente"
            else:
                pessoa = Pessoa.objects.filter(cpf=cpf)
                if pessoa:
                    lista_erros['cpf'] = "Este CPF Já está Registrado"
    else:
        lista_erros['cpf'] = "CPF incompleto informe todos os 11 dígitos"



def validar_termo(termo,data_termo,lista_erros):
    if termo and data_termo is None :
        lista_erros['data_termo'] = "Informe a data que consta no termo de entrega"
    return lista_erros
