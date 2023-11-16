from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Profile, Post
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render(request, 'index.html', {'user_profile': user_profile}) #chama o caminho para o html index

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username'] #insere na base
        email = request.POST['email'] #insere na base
        password = request.POST['password'] #insere na base
        password2 = request.POST['password2'] #insere na base
        if password == password2:
            if User.objects.filter(email=email).exists(): #Verifica se email ja existe
                messages.info(request, 'Email já cadastrado')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Usuário já cadastrado')
                return redirect('signup')
            else:
                # Cria o usuário
                user = User.objects.create_user(username = username, email=email, password=password)
                user.save()

                #logar e redirecionar para a pagina de  configuracao do usuario
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #Criar um perfil para o usuario
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings') #vai para a pagina de login
        else:
            messages.info(request, 'As senhas estão diferentes')
            return redirect('signup')

    else:
        return render(request, 'signup.html') #chama o caminho para o html index; se não tiver entrado no if, só mostra isso

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username, password=password) #verifica se esta no database
        if user is not None: #Se estiver
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Usuário não cadastrado')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') ==None:
            image = user_profile.profileimg
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})