from . models import *


def create_change_campos(lista_dados, tecnico, tabela, id_alterado, indicador):
    acao_change = Alteracao.objects.create(tipo_acao="2",id_alterado=id_alterado,
                                                indicador_alterado=indicador,tabela=tabela, responsavel=tecnico)
    for data_change in lista_dados:
        CampoChange.objects.create(campo=data_change.campo, novo_valor=data_change.valor_novo,
                                   antigo_valor=data_change.valor_antigo, modificacao=acao_change)


def create_adicao_tabela(data_modify, tecnico,acao):
    if acao == "Adicionar":
        acao_change = Acao.objects.create(tipo_acao="1", responsavel=tecnico)
    elif acao == "Excluir":
        acao_change = Acao.objects.create(tipo_acao="3", responsavel=tecnico)
    TabelaDadosChange.objetcs.create(tabela=data_modify.tabela, relacao=data_modify.relacao,modificacao=acao_change)
