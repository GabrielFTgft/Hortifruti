from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_django
from django.contrib import messages
from django.contrib.auth.models import User
from . import models

# Login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            user = User.objects.get(email=email)  # Tenta encontrar o usuário pelo email
            user_authenticated = authenticate(username=user.username, password=senha)

            if user_authenticated:
                login_django(request, user_authenticated)
                return redirect('produtos') 
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'login.html')

# Cadastro
def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se o usuário já está cadastrado
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Já existe um usuário com esse email.')
            return render(request, 'cadastro.html')

        # Cria o usuário
        user = User.objects.create_user(username=email, email=email, password=senha)
        user.save()

        # Opcional: Criar um cliente associado
        models.Cliente.objects.create(user=user, nome=nome, email=email)

        messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
        return redirect('login')

    return render(request, 'cadastro.html')

def principal(request):
    return render(request, 'principal.html')