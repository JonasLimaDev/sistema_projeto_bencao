from django import forms

from django.utils.html import format_html 
from .models import *
from datetime import date
# from .validations import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Primeiro Nome" )
    last_name = forms.CharField(max_length=40, required=True, label="Sobrenome")
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email',  'password1', 'password2', )
        help_texts = {
            'username': format_html('<ul><li>identificação para acesso.</li><li>use até 150 caracteres.</li><li>Letras, números e @.+-_ apenas.</li></ul>'),
            
        }


class FormTecnico(forms.ModelForm):
    class Meta:
        model = Tecnico
        widgets = {
            'data_nascimento': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date', }),

        }
        exclude = ['usuario','cadastro_pendente','data_registro']

    # def clean(self):
    #     lista_erros = {}
    #     try:
    #         cpf = self.cleaned_data["cpf"]
    #         if cpf != None:
    #             validar_cpf(cpf, lista_erros)
    #         data_nascimento = self.cleaned_data["data_nascimento"]
    #         if data_nascimento > date.today():
    #             lista_erros['data_nascimento'] = "Não é possível registrar pessoas nascidas no futuro"
    #     except:
    #         pass
    #     nome = self.cleaned_data["nome"]
    #
    #     if nome == "josé":
    #         lista_erros['nome'] = "aí não zé"
    #
    #     if lista_erros is not None:
    #         for erro in lista_erros:
    #             mensagem = lista_erros[erro]
    #             self.add_error(erro, mensagem)
    #
    #     return self.cleaned_data
