from django import forms
from .models import *
from datetime import date
from .validations import *

class FormReferencia(forms.ModelForm):
    class Meta:
        model = Referencia
        widgets ={
           'data_nascimento':forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date',}),
        }
        fields = ['nome','apelido','situacao_civil','sexo','identidade_genero', 'nome_social','data_nascimento',
        'cpf','nis','cadastro_unico','escolaridade','cor_raca','contato','contato2','trabalho','renda']
        # field_order = 
        help_texts = {
            'cpf': 'digite apenas os 11 números sem ponto ou espaço',
            'renda': 'Valor da contribuição com a renda total em R$',
        }
   
    def clean(self):
        lista_erros = {}
        try:
            cpf = self.cleaned_data["cpf"]
            if cpf != None:
                validar_cpf(cpf,lista_erros)
            data_nascimento = self.cleaned_data["data_nascimento"]
            if data_nascimento > date.today():
                lista_erros['data_nascimento'] = "Não é possível registrar pessoas nascidas no futuro"
        except:
            pass
        nome = self.cleaned_data["nome"]
        
        if nome == "josé":
            lista_erros['nome'] = "aí não zé"
        

        if lista_erros is not None:
            for erro  in lista_erros:
                mensagem = lista_erros[erro]
                self.add_error(erro, mensagem)

        return self.cleaned_data


class FormEditarReferencia(forms.ModelForm):
    class Meta:
        model = Referencia
        widgets = {
            'data_nascimento': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', }),

        }
        fields = ['nome','apelido','situacao_civil','sexo','identidade_genero', 'nome_social','data_nascimento',
        'cpf','nis','cadastro_unico','escolaridade','cor_raca','contato','contato2','trabalho','renda']
        help_texts = {
            'cpf': 'digite apenas os 11 números sem ponto ou espaço',
            'renda': 'Valor da contribuição com a renda total em R$',
        }

    def clean(self):
        lista_erros = {}
        try:
            cpf = self.cleaned_data["cpf"]
            if cpf != None:
                validar_cpf(cpf, lista_erros, NEW=False)
            data_nascimento = self.cleaned_data["data_nascimento"]
            if data_nascimento > date.today():
                lista_erros['data_nascimento'] = "Não é possível registrar pessoas nascidas no futuro"
        except:
            pass
        nome = self.cleaned_data["nome"]

        if nome == "josé":
            lista_erros['nome'] = "aí não zé"

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem = lista_erros[erro]
                self.add_error(erro, mensagem)

        return self.cleaned_data


class FormHabitacao(forms.ModelForm):
    class Meta:
        model = Habitacao
       
        fields = '__all__'
        help_texts = {
        'equipamento_comunitario': 'Segure a tecla "Ctrl" para selecionar vários',
        'complemento': 'Casa 05; 2º Andar; Chácara Conceição',
        'tempo_ocupacao':"Tempo de ocupação em anos. caso o residente esteja menos de um ano, atribuir zero"
        }
        

class FormEndereco(forms.ModelForm):
    
    class Meta:
       
        model = Endereco
        fields = '__all__'

        help_texts = {
        'logradouro': 'Ex: Av. João Paulo II; Rua José Ribeiro Alves; Tv. Sergipe',
        'complemento': 'Casa 05; 2º Andar; Chácara Conceição',
        }


class FormInfoExtra(forms.ModelForm):
    class Meta:
        model = Identificacao
        fields = '__all__'
        widgets = {
            'data_emissao': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', }),
        }

        help_texts = {
        'natural_cidade': 'Cidade em que a pessoa nasceu',
        'complemento': 'Casa 05; 2º Andar; Chácara Conceição',
        }


class FormDadosEducacao(forms.ModelForm):
    class Meta:
        model = DadosEducacao
        fields = '__all__'
        widgets = {
            'data_emissao': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', }),
        }

        help_texts = {
        'natural_cidade': 'Cidade em que a pessoa nasceu',
        'complemento': 'Casa 05; 2º Andar; Chácara Conceição',
        }


class FormMembro(forms.ModelForm):
    class Meta:
        model = Membros
        widgets ={
           'data_nascimento':forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date',}),
            
        }
        exclude = ['cadastro_membro','dados_educacionais']
        help_texts = {
            'cpf': 'digite apenas os 11 números sem ponto ou espaço',
            'parentesco': 'Parentesco em relação à Referência Familiar',
            'renda': 'Valor da contribuição com a renda total em R$',
        }
   
    def clean(self):
        lista_erros = {}
        try:
            cpf = self.cleaned_data["cpf"]
            if cpf != None:
                validar_cpf(cpf, lista_erros, NEW=True)
        except:
            pass
        try:
            data_nascimento = self.cleaned_data["data_nascimento"]
            if data_nascimento > date.today():
                lista_erros['data_nascimento'] = "Não é possível registrar pessoas nascidas no futuro"
        except:
            pass
        nome = self.cleaned_data["nome"]
        if nome == "josé":
            lista_erros['nome'] = "aí não zé"
        if lista_erros is not None:
            for erro  in lista_erros:
                mensagem = lista_erros[erro]
                self.add_error(erro, mensagem)

        return self.cleaned_data  


class FormEditarMembro(forms.ModelForm):
    class Meta:
        model = Membros
        widgets ={
           'data_nascimento':forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date',}),
            
        }
        exclude = ['cadastro_membro']
        help_texts = {
            'cpf': 'digite apenas os 11 números sem ponto ou espaço',
            'parentesco': 'Parentesco em relação ao Responsável Familiar',
            'renda': 'Valor da contribuição com a renda total em R$',
        }
   
    def clean(self):
        lista_erros = {}
        
        try:
            cpf = self.cleaned_data["cpf"]
            if cpf != None:
                validar_cpf(cpf,lista_erros,NEW=False)
        except:
            pass
        nome = self.cleaned_data["nome"]
        
        try:
            data_nascimento = self.cleaned_data["data_nascimento"]
            if data_nascimento > date.today():
                lista_erros['data_nascimento'] = "Não é possível registrar pessoas nascidas no futuro"
        except:
            pass
        
        if nome == "josé":
            lista_erros['nome'] = "aí não zé"
        
        if lista_erros is not None:
            for erro  in lista_erros:
                mensagem = lista_erros[erro]
                self.add_error(erro, mensagem)

        return self.cleaned_data  


class FormDadosCadastro(forms.Form):
    responsavel = forms.CharField(label="Referência Familiar")
    responsavel.widget.attrs['disabled'] = 'disabled'
    responsavel.widget.attrs["readonly"] = True
    bairro = forms.CharField(label="Bairro")
    bairro.widget.attrs['disabled'] = 'disabled'
    bairro.widget.attrs["readonly"] = True


DOCS_CHOICES =(
    ("1", "Bairros"),
    ("2", "Pessoas"),
)


class FormUploadDados(forms.Form):
    # beneficiado.widget.attrs['disabled'] = 'disabled'
    tipo_informacoes = forms.ChoiceField(choices = DOCS_CHOICES)
    arquivo_dados = forms.FileField(label='Arquivo com os dados',required=True)
    arquivo_dados.widget.attrs={'class':'form-control','placeholder':arquivo_dados.label,'accept':'.json'}
