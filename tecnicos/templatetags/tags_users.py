from django import template
register = template.Library()

from ..models import Tecnico
from django.contrib.auth.models import User


@register.filter(name='is_supervisor')
def is_supervisor(value):
	user = User.objects.get(id=int(value))
	if user.groups.filter(name='Supervisor').exists():
		return True
	else:
		return False


@register.filter(name='estilo_tec_card')
def estilo_tec_card(value):
	tecnico = Tecnico.objects.get(id=value)
	if tecnico.cadastro_pendente and not tecnico.usuario.is_active:
		return "border-danger"
	elif not tecnico.cadastro_pendente and not tecnico.usuario.is_active:
		return "border-warning"
	else:
		return ""

@register.filter(name='tecnicos_pendentes')
def tecnicos_pendentes(value):
	tecnicos = Tecnico.objects.all()
	tecnico_pendente = 0
	user = User.objects.get(id=value)
	for tecnico in tecnicos:
		if tecnico.cadastro_pendente:
			tecnico_pendente+=1
	if user.groups.filter(name='Supervisor').exists():
		value = tecnico_pendente
		return value
	else:
		return ""
