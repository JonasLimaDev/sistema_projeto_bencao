from django.db import models
from datetime import datetime


ESCOLHA = (
    ('1', 'Sim'),
    ('2', 'Não'),
    )
    
# Create your models here.
class Bairro(models.Model):
    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=75, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nome


class EquipamentoComunitario(models.Model):
    class Meta:
        verbose_name = "Equipamento Comunitário"
        verbose_name_plural = "Equipamentos Comunitários"        
    nome_equipamento = models.CharField(max_length=25, null=False, blank=False, verbose_name="Equipamento Comunitário")
    
    def __str__(self):
        return self.nome_equipamento


class Pessoa(models.Model):
    class Meta:
        # abstract = True
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ('nome',)


    SEXO = (
        ('1', 'Feminino'),
        ('2', 'Masculino'),
    )

    ESCOLARIDADE = (
        ('1', 'Não Alfabetizado'),
        ('2', 'Fundamental Incompleto'),
        ('3', 'Fundamental Completo'),
        ('4', 'Ensino Médio Incompleto'),
        ('5', 'Ensino Médio Completo'),
        ('6', 'Ensino Superior Incompleto'),
        ('7', 'Ensino Superior Completo'),
    )

    TRABALHO = (
        ('1', 'Não Trabalha'),
        ('2', 'Trabalhador Por Conta Própria'),
        ('3', 'Trabalhador Temporário em Área Rural'),
        ('4', 'Empregado Sem Carteira de Trabalho Assinada'),
        ('5', 'Empregado Com Carteira de Trabalho Assinada'),
        ('6', 'Trabalhador Doméstico Sem Carteira de Trabalho Assinada'),
        ('7', 'Trabalhador Não Remunerado'),
        ('8', 'Estagiário'),
        ('9', 'Aprendiz'),
        ('10', 'Aposentado'),
        ('11', 'Pensionista'),
    )

    nome = models.CharField(max_length=150, null=False, blank=False)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.CharField(max_length=1, choices=SEXO, null=False, blank=False)
    trabalho = models.CharField(max_length=2, choices=TRABALHO, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=True, blank=True, verbose_name="CPF", unique=True)
    nis = models.CharField(max_length=11, null=True, blank=True, verbose_name="NIS")
    escolaridade = models.CharField(max_length=1, choices=ESCOLARIDADE, null=False, blank=False)
    # profissao = models.CharField(max_length=45, null=True, blank=True,verbose_name="Profissão ou Formação Técnica")
    contato = models.CharField(max_length=15, null=True, blank=True)
    renda = models.FloatField(null=True, blank=True)
    dados_educacionais = models.OneToOneField('dados_adicionais.Educacao', null=True, blank=True, on_delete=models.CASCADE)
    dados_saude = models.OneToOneField('dados_adicionais.Saude', null=True, blank=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Referencia(Pessoa):
    class Meta:
        verbose_name = "Referência Familiar"
        verbose_name_plural = "Referências Familiares"

    
    ESTADO_CIVIL = (
        ('1', 'Solteiro(a)'),
        ('2', 'Casado(a)'),
        ('3', 'Divorciado(a)'),
        ('4', 'Viúvo(a)'),
    )

    GENERO = (
        ('1', 'Cisgênero'),
        ('2', 'Transgênero'),
        ('3', 'Não Binário'),
        ('4', 'Não Declarado'),
    )

    COR_RACA = (
        ('1', 'Branca'),
        ('2', 'Preta'),
        ('3', 'Amarela'),
        ('4', 'Parda'),
        ('5', 'Indígena')
    )
    #apelido = models.CharField(max_length=30, null=True, blank=True)

    identidade_genero = models.CharField(max_length=1, choices=GENERO, null=False, blank=False, verbose_name="Identidade de Gênero")
    apelido = models.CharField(max_length=20, null=True, blank=True)
    
    nome_social = models.CharField(max_length=30, null=True, blank=True,verbose_name="Nome Social")
    situacao_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL, null=False, blank=False, verbose_name="Situação Civil")
    cor_raca = models.CharField(max_length=1, choices=COR_RACA, null=False, blank=False, verbose_name="Identificação Étnico-Racial")
    
    documentos_extras = models.OneToOneField('dados_adicionais.Identificacao', null=True, blank=True, on_delete=models.CASCADE)
    cadastro_unico = models.CharField(max_length=1, choices=ESCOLHA, null=False, blank=False,default='1', verbose_name="Possui Cadastro Único?")
    
    contato2 = models.CharField(max_length=15, null=True, blank=True, verbose_name="Contato Alternativo")
    

class Membros(Pessoa):
    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    PARENTESCO = (
        ('1', 'Esposa(o)'),
        ('2', 'Filho(a)'),
        ('3', 'Neto(a)'),
        ('4', 'Sobrinho(a)'),
        ('5', 'Mãe/Pai'),
        ('6', 'Avó/Avô'),
        ('7', 'Tio(a)'),
        ('8', 'Outro'),
    )

    cadastro_membro = models.ForeignKey("Cadastro", on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=2, choices=PARENTESCO, null=False, blank=False, default='2')


class Identificacao(models.Model):
    ESTADOS = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ","Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )
    rg = models.CharField(max_length=16, null=False, blank=False, verbose_name="Nº RG")
    orgao_emissor = models.CharField(max_length=25, null=False, blank=False, verbose_name="Órgão Emissor (RG)")
    data_emissao = models.DateField(verbose_name="Data de Emissão (RG)")
    titulo_eleitor = models.CharField(max_length=25, null=False, blank=False, verbose_name="Nº Titulo de Eleitor")
    zona = models.CharField(max_length=5, null=False, blank=False, verbose_name="Zona Eleitoral")
    secao = models.CharField(max_length=5, null=False, blank=False, verbose_name="Seção Eleitoral")
    natural_cidade = models.CharField(max_length=50, null=False, blank=False, verbose_name="Cidade de Naturalidade")
    natural_estado = models.CharField(max_length=2, choices=ESTADOS, null=False, blank=False, verbose_name="Estado Naturalidade")
    
    def __str__(self):
        return self.rg


class Habitacao(models.Model):
    class Meta:
        verbose_name = "Habitação"
        verbose_name_plural = "Habitações"

    MORADIA = (
        ('1', 'Alugada'),
        ('2', 'Própria'),
        ('3', 'Cedida'),
        ('4', 'Invasão'),
        ('5', 'Sem Moradia Fixa'),
    )

    COSNTRUCAO = (
        ('1', 'Alvenaria'),
        ('2', 'Barro'),
        ('3', 'Madeira'),
        ('4', 'Outro'),
        ('5', 'Não Se Aplica'),
    )

    TELHADO = (
        ('1', 'Brasilit'),
        ('2', 'Telha de Barro'),
        ('3', 'Lage'),
        ('4', 'Outro'),
        ('5', 'Não Se Aplica'),
    )

    ELETRICIDADE = (
        ('1', 'Com Medidor Próprio'),
        ('2', 'Sem Padrão'),
        ('3', 'Não Possui'),
    )

    ABASTECIMENTO = (
        ('1', 'Rede Geral de Distribuição'),
        ('2', 'Poço'),
        ('3', 'Fonte, Nascente ou Mina'),
        ('4', ' Carro-Pipa'),
        ('5', 'Água da Chuva Armazenada'),
        ('6', ' Rios, Açudes, Córregos, Lagos e Igarapés'),
        ('7', 'Outra'),
    )

    ESGOTO = (
        ('1', 'Rede Geral ou Pluvial'),
        ('2', 'Fossa Rudimentar ou Buraco'),
        ('3', 'Vala'),
        ('4', 'Não Possui'),
    )

    COLETA = (
        ('1', 'Coletado no Domicílio Por Serviço de Limpeza'),
        ('2', 'Depositado em Caçamba de Serviço de Limpeza '),
        ('3', 'Queimado na Propriedade'),
        ('4', 'Enterrado na Propriedade'),
        ('5', 'Jogado em Terreno Baldio, Encosta ou Área Pública'),
        ('6', 'Outro Destino'),
    )

    PAVIMENTO = (
        ('1', 'Asfalto'),
        ('2', 'Bloqueteamento'),
        ('3', 'Não Possui'),
    )


    situacao_moradia = models.CharField(max_length=1, choices=MORADIA, null=False, blank=False,
                                        verbose_name="Situação da Moradia")
    tipo_construcao = models.CharField(max_length=1, choices=COSNTRUCAO, null=False, blank=False,
                                        verbose_name="Tipo de Construção")
    rede_eletrica = models.CharField(max_length=1, choices=ELETRICIDADE, null=False, blank=False,
                                        verbose_name="Possui Energia Elétrica")
    possui_abastecimento = models.CharField(max_length=1, choices=ABASTECIMENTO, null=False, blank=False,
                                        verbose_name="Abastecimento de Água")
    possui_rede_esgoto = models.CharField(max_length=1, choices=ESGOTO, null=False, blank=False,
                                        verbose_name="Possui Rede de Esgoto")
    possui_coleta = models.CharField(max_length=1, choices=COLETA, null=False, blank=False,
                                        verbose_name="Coleta de Lixo")
    pavimentacao = models.CharField(max_length=1, choices=PAVIMENTO, null=False, blank=False,
                                        verbose_name="Pavimentação da Rua")
    
    tempo_ocupacao = models.IntegerField(null=False, blank=False, verbose_name="Tempo de Ocupação do Imóvel")
    numero_moradores = models.IntegerField(null=False, blank=False, verbose_name="Número de Moradores")
    numero_comodos = models.IntegerField(null=False, blank=False, verbose_name="Número de Cômodos")
    equipamento_comunitario = models.ManyToManyField(EquipamentoComunitario,verbose_name="Equipamento Comunitários Próximos")
    
    def __str__(self):
        return self.situacao_moradia


class Endereco(models.Model):
    class Meta:
        ordering = ('bairro__nome',)

    logradouro = models.CharField(max_length=100, null=False, blank=False)
    numero = models.CharField(max_length=35, null=True, blank=True)
    complemento = models.CharField(max_length=170, null=True, blank=True)
    ponto_referencia = models.CharField(max_length=250, null=True, blank=True, verbose_name="Ponto de Referência")
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    cep = models.CharField(max_length=15, null=True, blank=True, verbose_name="CEP")

    def __str__(self):
        return self.logradouro


class Cadastro(models.Model):
    CRAS = (
        ('1','CRAS I'),
        ('2','CRAS II'),
        ('3','CRAS III'),
        )

    class Meta:
        ordering = ('responsavel_familiar__nome',)
    
    responsavel_familiar = models.OneToOneField(Referencia, on_delete=models.CASCADE)
    habitacao = models.OneToOneField(Habitacao, on_delete=models.CASCADE)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)
    responsavel_cadastro = models.ForeignKey("tecnicos.Tecnico", on_delete=models.PROTECT, default=1)
    abrangencia = models.CharField(max_length=1, choices=CRAS, null=True, blank=True, verbose_name="Cras de Abrangência")
    data_cadastro = models.DateField(null=False, blank=False, default=datetime.now)
    data_alteracao = models.DateField(auto_now=True,null=False, blank=False, )
    entrevistador = models.CharField(max_length=200, null=True, blank=True, verbose_name="Entrevistador")

    def __str__(self):
        return self.responsavel_familiar.nome


