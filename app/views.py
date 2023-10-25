from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.models import User
from app.forms import RegistrarUsuarioForm
from django.contrib.auth import authenticate, login, logout
#from perfis.models import Perfil
from django.contrib import messages

# Create your views here.
class RegistrarUsuarioView(View):
    template_name = 'app/registrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['email'],
                                                email=dados_form['email'],
                                                password=dados_form['senha'])

            #perfil = Perfil(nome=dados_form['nome'],
                            #usuario=usuario)
            #perfil.save()
            messages.add_message(request, messages.INFO, 'Usuário cadastrado com sucesso')
            return redirect('login')
        return render(request, self.template_name, {'form': form})

class LoginUsuarioView(View):
    template_name = 'app/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)

        if user is None:
            if User.objects.filter(email=username):
                messages.add_message(request, messages.INFO, 'Usuário bloqueado.')
            else:
                messages.add_message(request, messages.INFO, 'Usuário não cadastrado.')
        else:
            login(request, user)
            return redirect('index')

        return redirect('login')


'''
#página inicial
def home(request):
    return render(request,'home.html')

#formulário de cadastro
def create(request):
    return render(request,'create.html')

#insere usuários no banco
def store(request):
    data={}
    if(request.POST['password'] != request.POST['password-conf']):
        data['msg'] = 'Senha e confirmação de senha diferentes!'
        data['class'] = 'alert-danger'
    else:
        user = User.objects.create_user(request.POST['name'],request.POST['email'],request.POST['password'])
        user.first_name = request.POST['name']
        user.username = request.POST['user']
        user.save()
        data['msg'] = 'Usuário cadastrado com sucesso!'
        data['class'] = 'alert-success'
    return render(request,'painel.html',data)

#formulário de login
def painel(request):
    return render(request,'painel.html')

#processa o login
def dologin(request):
    data = {}
    user = authenticate(username=request.POST['user'],password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('/dashboard/')
    else:
        data['msg'] = 'Usuário ou senha inválidos'
        data['class'] = 'alert-danger'
        return render(request,'painel.html', data)

#página inicial
def dashboard(request):
    return render(request,'dashboard/home.html')


#logout
def logouts(request):
    logout(request)
    return redirect('/painel/')
'''