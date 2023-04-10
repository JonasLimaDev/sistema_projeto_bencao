from django.db import models

ESCOLHA = (
    ('1', 'Sim'),
    ('2', 'Não'),
    )

# Create your models here.
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
        ("RJ", "Rio de Janeiro"),
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
    natural_estado = models.CharField(max_length=2, choices=ESTADOS, null=False, blank=False,
                                      verbose_name="Estado Naturalidade")

    def __str__(self):
        return self.rg


class Educacao(models.Model):
    class Meta:
        verbose_name = "Dado de Educação"
        verbose_name_plural = "Dados Educacionais"

    NIVEL_ESTUDO = (
        ('1', 'Alfabetização'),
        ('2', 'Ensino Infantil'),
        ('3', 'Ensino Fundamental'),
        ('4', 'Ensino Médio'),
        ('5', 'Ensino Técnico'),
        ('6', 'Ensino Superior'),
        ('7', 'Pós Graduação'),
        ('8', 'Outro'),
        ('9', 'Nenhum'),
    )

    estuda = models.CharField(max_length=1, choices=ESCOLHA, null=False, blank=False, verbose_name="Está Estudando?")
    nivel_curso = models.CharField(max_length=1, choices=NIVEL_ESTUDO, null=True, blank=True,
                                   verbose_name="Está Cursando?")
    local = models.CharField(max_length=60, null=True, blank=True, verbose_name="Local Onde Estuda")


class Saude(models.Model):
    class Meta:
        verbose_name = "Dado de Saúde"
        verbose_name_plural = "Dados Saúde"

    TIPO_DEFICIENCIA = (
        ('1', 'Física'),
        ('2', 'Auditiva'),
        ('3', 'Visual'),
        ('4', 'Mental/Intelectual'),
        ('5', 'Múltipla'),
    )

    GRAVIDEZ = (
        ('1', 'Gravida'),
        ('2', 'Não Grávida'),
        ('3', 'Não Se Aplica'),
    )

    deficiencia = models.CharField(max_length=1, choices=ESCOLHA, null=False, blank=False,
                                   verbose_name="Possui Deficiência?")
    tipo_deficiencia = models.CharField(max_length=1, choices=TIPO_DEFICIENCIA, null=True, blank=True,
                                        verbose_name="Especifique o Tipo de Deficiência")
    gravidez = models.CharField(max_length=1, choices=GRAVIDEZ, null=True, blank=True, verbose_name="Gravidez")


class DadosBanco(models.Model):
    class Meta:
        verbose_name = "Dados de Banco"
        verbose_name_plural = "Dados Bancários"

    conta = models.CharField(max_length=9,  null=False, blank=False, verbose_name="Nº da Conta")
    agencia = models.CharField(max_length=5,  null=False, blank=False, verbose_name="Agência")