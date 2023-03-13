from .models import CampoChange, TabelaDadosChange
class ChangeCampoData():
    def __init__(self, campo, valor_antigo, valor_novo):
        self.campo = campo
        self.valor_antigo = valor_antigo
        self.valor_novo = valor_novo


class ChangeTableData():
    def __init__(self, table, relacao):
        self.table = table
        self.relacao = relacao
        # self.valor_novo = valor_novo


class DataAlteracoes():
    def __init__(self,alteracao_bd):
        self.id = alteracao_bd.id
        self.tipo_acao = alteracao_bd.get_tipo_acao_display()
        self.data_modificacao = alteracao_bd.data_modificacao
        self.responsavel = alteracao_bd.responsavel

        self.campos_modificados = self.get_data_campo_modified()
        self.tablas_modificadas = self.get_data_table_modified()

    def get_data_campo_modified(self):
        lista_campos = CampoChange.objects.filter(modificacao__id=self.id)
        if lista_campos:
            return lista_campos
        else:
            return None

    def get_data_table_modified(self):
        lista_dados = TabelaDadosChange.objects.filter(modificacao__id=self.id)
        if lista_dados:
            return lista_dados
        else:
            return None

