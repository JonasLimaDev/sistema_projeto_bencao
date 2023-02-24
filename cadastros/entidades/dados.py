from ..models import Membros
from datetime import date


class Referencia():
    def __init__(self, referencia_bd):
        self.id = referencia_bd.id
        self.nome = referencia_bd.nome
        self.apelido = referencia_bd.apelido if referencia_bd.apelido else "Não Possui"
        self.nome_social = referencia_bd.nome_social if referencia_bd.nome_social else "Não Possui"
        self.identidade_genero =  referencia_bd.get_identidade_genero_display()

        self.situacao_civil = referencia_bd.get_situacao_civil_display()
        self.sexo = referencia_bd.get_sexo_display()
        self.data_nascimento = referencia_bd.data_nascimento
        self.idade = int((date.today() - self.data_nascimento).days / 365.25)
        self.cpf = self.formatar_cpf(referencia_bd.cpf)
        self.nis = referencia_bd.nis if referencia_bd.nis else "Não Informado"
        self.cadastro_unico = referencia_bd.get_cadastro_unico_display()
        self.cor_raca = referencia_bd.get_cor_raca_display()
        self.escolaridade = referencia_bd.get_escolaridade_display()
        self.trabalho = referencia_bd.get_trabalho_display()
        self.contato = referencia_bd.contato if referencia_bd.contato else "Não Informado"
        self.contato2 = referencia_bd.contato2 if referencia_bd.contato2 else "-" 
        self.renda = referencia_bd.renda
        self.info_extra = referencia_bd.documentos_extras
        self.dados_educacionais = referencia_bd.dados_educacionais
        self.dados_saude = referencia_bd.dados_saude

        self.all_data = {            
            "Nome":self.nome,
            "Apelido":self.apelido,
            "Situação Civil":self.situacao_civil,
            
            "Sexo":self.sexo,
            "Identidade de Gênero":self.identidade_genero,
            "Nome Social":self.nome_social,
            
            "Data de Nascimento":self.data_nascimento,
            "Idade":self.idade,
            "CPF":self.cpf,
            "NIS":self.nis,
            "Possui Cadastro Único":self.cadastro_unico,

            "Escolaridade":self.escolaridade,
            "Identificação Étnico-Racial":self.cor_raca,
            
            "Contato Principal":self.contato,
            "Contato Alternativo":self.contato2,
            "Situação de Trabalho":self.trabalho,
            "Renda":self.renda,
            
        }
        if self.info_extra:
            self.extra_all_data = {
                "Nº RG": self.info_extra.rg,
                "Órgão Emissor (RG)": self.info_extra.orgao_emissor,
                "Data de Emissão (RG)": self.info_extra.data_emissao,
                "Nº Titulo de Eleitor": self.info_extra.titulo_eleitor,
                "Zona Eleitoral": self.info_extra.zona,
                "Seção Eleitoral": self.info_extra.secao,
                "Cidade de Naturalidade": self.info_extra.natural_cidade,
                "Estado Naturalidade": self.info_extra.natural_estado,
            
            }
        if self.dados_educacionais:
            self.educacao_all_data = {
                "Está Estudando?": self.dados_educacionais.get_estuda_display(), 
                "Está Cursando?": self.dados_educacionais.get_nivel_curso_display(),
                "Local Onde Estuda": self.dados_educacionais.local
            }
        if self.dados_saude:
            self.saude_all_data = {
                "Possui Deficiência?": self.dados_saude.get_deficiencia_display(),
                "Tipo de Deficiência": self.dados_saude.get_tipo_deficiencia_display(),
                "Pessoa Grávida": self.dados_saude.get_gravidez_display()
            }
        
    def formatar_cpf(self,value):
        if value:
            value = value[0:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:]
        else:
            value = "Não Informado"
        return value


class Membro():
    def __init__(self, membro_bd):
        self.id = membro_bd.id
        self.nome = membro_bd.nome
        
        # self.situacao_civil = "-"
        self.sexo = membro_bd.get_sexo_display()
        self.data_nascimento = membro_bd.data_nascimento
        self.idade = int((date.today()-self.data_nascimento).days / 365.25)
        self.cpf = self.formatar_cpf(membro_bd.cpf)
        self.nis = membro_bd.nis if membro_bd.nis else "Não Informado" 
        self.escolaridade = membro_bd.get_escolaridade_display()
        self.trabalho = membro_bd.get_trabalho_display()
        self.contato = membro_bd.contato if membro_bd.contato else "Não Informado"
        # self.contato2 = membro_bd.contato2 if membro_bd.contato2 else "Não Informado"
        self.renda = membro_bd.renda
        self.parentesco = membro_bd.get_parentesco_display()
        self.dados_educacionais = membro_bd.dados_educacionais
        self.dados_saude = membro_bd.dados_saude
        

        self.all_data = {
            "Nome": self.nome,
            "Parentesco": self.parentesco,
            
            "Sexo": self.sexo,
            "Data de Nascimento": self.data_nascimento,
            "Idade": self.idade,
            
            "CPF": self.cpf,
            "NIS": self.nis,
            
            "Escolaridade": self.escolaridade,
            "Contato": self.contato,
            
            "Situação de Trabalho": self.trabalho,
            "Renda": self.renda
        }
        if self.dados_educacionais:
            self.educacao_all_data = {
                "Está Estudando": self.dados_educacionais.get_estuda_display(), 
                "Está Cursando": self.dados_educacionais.get_nivel_curso_display(),
                "Local Onde Estuda": self.dados_educacionais.local
            }
        if self.dados_saude:
            self.saude_all_data = {
                "Possui Deficiência?": self.dados_saude.get_deficiencia_display(),
                "Tipo de Deficiência": self.dados_saude.get_tipo_deficiencia_display(),
                "Pessoa Grávida": self.dados_saude.get_gravidez_display()
            }

    def formatar_cpf(self,value):
        if value:
            value = value[0:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:]
        else:
            value = "Não Informado"
        return value


class Cadastro():
    def __init__(self,cadastro_bd):
        self.id = cadastro_bd.id
        self.responsavel = Referencia(cadastro_bd.responsavel_familiar) 
        self.endereco = cadastro_bd.endereco
        self.habitacao = cadastro_bd.habitacao
        self.data_cadastro = cadastro_bd.data_cadastro
        self.data_alteracao = cadastro_bd.data_alteracao
        self.abrangencia = cadastro_bd.get_abrangencia_display()
        self.entrevistador = cadastro_bd.entrevistador
        #self.responsavel_cadastro = cadastro_bd.responsavel_cadastro
        self.lista_membros = [Membro(membro_obj) for membro_obj in Membros.objects.all().filter(cadastro_membro=cadastro_bd)]
        self.renda_total = self.calcular_renda()
        self.renda_per_capita = self.calcular_renda_per_capita()
        self.disparidades = self.disparidade()

        self.all_data = {            
            "Data do Cadastro":self.data_cadastro,
            "Ultima Alteração":self.data_alteracao,
            "Abrangência":self.abrangencia,
            "Entrevistador":self.entrevistador,
            
        }
        self.dados_renda = {            
            "Renda Total da Familia":self.renda_total,
            "Renda Per Capita":self.renda_per_capita,
        }

    def calcular_renda(self):
        renda = 0
        renda += float(self.responsavel.renda) if self.responsavel.renda else 0 
        for membro in self.lista_membros:
            renda += float(membro.renda)  if membro.renda else 0
        return renda
    
    def calcular_renda_per_capita(self):
        renda = self.calcular_renda()
        renda_per_capita = renda / self.habitacao.numero_moradores
        return renda_per_capita

    def disparidade(self):
        membros_cd = len(self.lista_membros)+1
        self.habitacao.numero_moradores
        if membros_cd < self.habitacao.numero_moradores:
            disparidade = f"Falta Membros no Cadastro {membros_cd} de {self.habitacao.numero_moradores}"
        elif membros_cd > self.habitacao.numero_moradores:
            disparidade = f"Mais Membros Que no  Cadastro {membros_cd} de {self.habitacao.numero_moradores}"
        else:
            disparidade = None
        return disparidade
            