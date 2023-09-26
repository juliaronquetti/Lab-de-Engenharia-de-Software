from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
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
    user = authenticate(username=request.POST['user'],password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('/dashboard/')
    else:
        return render(request,'painel.html')

#página inicial
def dashboard(request):
    return render(request,'dashboard/home.html')
