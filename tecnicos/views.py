from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import FormTecnico, SignUpForm
from .models import Tecnico
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.



class CriarUsusarioView(TemplateView):
    form_class_usuario = SignUpForm
    form_class_tecnico = FormTecnico
    template_name = "tecnicos/formulario_login.html"
    context = {'titulo_pagina': "Cadastro de Usuário do Sistema"}

    def get(self, request, *args, **kwargs):
        forms_generic = {"Informações de Acesso":  self.form_class_usuario(),
                         "Informações de Trabalho": self.form_class_tecnico()}
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form1 = self.form_class_usuario(request.POST)
        form2 = self.form_class_tecnico(request.POST)
        forms_generic = {"Informações de Acesso": form1, "Informações de Trabalho": form2}
        self.context['forms_generic'] = forms_generic
        if form1.is_valid():
            if form2.is_valid():    
                form1.save()
                user = User.objects.get(username=form1.cleaned_data['username'])
                user.is_active = False
                user.save()
                orgao_form = form2.cleaned_data['orgao']
                cargo_form = form2.cleaned_data['cargo']
                contato_form = form2.cleaned_data['contato']
                Tecnico.objects.create(usuario=user, orgao=orgao_form, cargo=cargo_form,
                                       contato=contato_form, cadastro_pendente=True)
                messages.error(request, 'Usuario Cadastrado Com Sucesso, aguarde a autorização')
                return redirect('home')
                # return render(request, self.template_name,self.context)
        return render(request, self.template_name, self.context)


class LoginView(TemplateView):
    template_name = "tecnicos/formulario_login.html"
    form_class_logar = AuthenticationForm
    context = {'titulo_pagina': "Logar-se no Sistema",'login':True}

    def get(self, request, *args, **kwargs):

        forms_generic = {"Informações de Acesso": self.form_class_logar()}
        self.context['forms_generic'] = forms_generic
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class_logar(request.POST)
        forms_generic = {"Informações de Acesso": form}
        self.context['forms_generic'] = forms_generic
        pagina_destino = self.request.GET['next'] if 'next' in self.request.GET else 'home'
        nome_usuario = request.POST["username"]
        senha = request.POST["password"]
        usuario = User.objects.all().filter(username=nome_usuario)
        if not usuario:
            messages.error(request, 'Usuario Não Cadastrado')
            return redirect('logar_usuario')
        elif not usuario[0].is_active:
            messages.error(request, 'Usuario Cadastrado, Mas Não Autorizado')
            return redirect('logar_usuario')
        else:
            usuario = authenticate(request, username=nome_usuario, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect(pagina_destino)
        else:
            messages.error(request, 'Senha Incorreta')
            return redirect('logar_usuario')
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class PerfilUsuarioView(TemplateView):
    template_name = "tecnicos/perfil.html"
    def get(self,request, *args, **kwargs):
        id = self.kwargs['pk']
        if id != request.user.id:
            id =  request.user.id
        user_bd = get_object_or_404(User,id=id)
        if user_bd != request.user:
            return redirect('home')
        dados = Tecnico.objects.get(usuario=user_bd)
        return render(request,self.template_name,{'tecnico':dados})


@method_decorator(login_required, name='dispatch')
class EquipeTecnicaView(TemplateView):
    template_name = "tecnicos/equipe.html"
    def get(self,request, *args, **kwargs):
        user = User.objects.get(id=int(request.user.id))
        if user.groups.filter(name='Supervisor').exists():
            supervisor = True if request.user.groups.filter(name='Supervisor').exists() else False
            tecnicos = Tecnico.objects.all()
            return render(request,self.template_name,{'tecnicos':tecnicos,'supervisor':supervisor})
        else:
            return redirect('dados_tecnico', user.id)
        
    
    def post(self,request, *args, **kwargs):
        supervisor = True if request.user.groups.filter(name='Supervisor').exists() else False
        tecnicos = Tecnico.objects.all()
        desativados = tecnicos.filter()
        grupos = {'1':"Agente",'2':"Supervisor"} 
        if 'desativar' in request.POST:
            id_tecnico = request.POST['id_tecnico']
            tecnico = tecnicos.filter(id=id_tecnico)[0]
            usuario = User.objects.get(id=tecnico.usuario.id)
            usuario.is_active = False
            usuario.save(force_update=True)
                
        if 'decidir' in request.POST:
            opcao = request.POST['escolha']
            id_tecnico = request.POST['id_tecnico']
            tecnico = tecnicos.filter(id=id_tecnico)[0]
            usuario = User.objects.get(id=tecnico.usuario.id)
            if opcao != '3':
                grupo = Group.objects.get(name=grupos[opcao])
                usuario.is_active = True
                usuario.groups.add(grupo)
                tecnico.cadastro_pendente=False
                usuario.save(force_update=True)
                tecnico.save(force_update=True)
            else:
                usuario.delete()
                tecnico.delete()
            return redirect("equipe_tecnica")
        return render(request,self.template_name,{'tecnicos':tecnicos,'supervisor':supervisor})



def logout_view(request):
    logout(request)
    return redirect('home')
