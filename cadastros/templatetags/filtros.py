from django import template
register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg):
	return value.as_widget(attrs={'class': arg})


@register.filter(name='formatar_cpf')
def formatar_cpf(value):
	if value:
		value = value[0:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:]
	else:
		value = "Não Informado"
	return value


@register.filter(name='formatar_reais')
def formatar_reais(value):
	if value != None and int(value) > 0:
		return f"R$ {value:.2f}".replace('.', ',')
	else:
		return "-"
