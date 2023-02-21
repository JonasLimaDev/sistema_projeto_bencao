
from .models import Tecnico
from django.contrib.auth.models import User

def tipo_usuario(user_rerquest):
    usuario = User.objects.get(id=user_rerquest.id)
    if usuario.groups.filter(name='Supervisor').exists():
        return "Supervisor"
    elif usuario.groups.filter(name='Coordenador').exists():
        return "Coordenador"
    elif usuario.groups.filter(name='Agente').exists():
        return "Agente"