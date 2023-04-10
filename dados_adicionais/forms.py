from django import forms
from .models import *

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
        model = Educacao
        fields = '__all__'

        help_texts = {
        # 'natural_cidade': 'Cidade em que a pessoa nasceu',
        # 'complemento': 'Casa 05; 2º Andar; Chácara Conceição',
        }


class FormDadosSaude(forms.ModelForm):
    class Meta:
        model = Saude
        fields = '__all__'

        help_texts = {
        # 'natural_cidade': 'Cidade em que a pessoa nasceu',
        # 'complemento': 'Casa 05; 2º Andar; Chácara Conceição',
        }


class FormDadosBancarios(forms.ModelForm):
    class Meta:
        model = DadosBanco
        fields = '__all__'

