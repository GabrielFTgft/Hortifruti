from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login as login_django
# from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente

# Login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            # Tenta buscar o cliente pelo e-mail
            cliente = Cliente.objects.get(email=email)

            # Verifica se a senha está correta
            if cliente.senha == senha:
                 # Armazena o ID do cliente na sessão
                request.session['cliente_id'] = cliente.id
                request.session['cliente_nome'] = cliente.nome

                # Redireciona para a página de produtos (ou outra página principal)
                return redirect('produtos')
            else:
                messages.error(request, 'Senha inválida.')
        except Cliente.DoesNotExist:
            # Caso o cliente com o e-mail fornecido não exista
            messages.error(request, 'Usuário não encontrado.')

    # Renderiza a página de login se for um GET ou se houver erro
    return render(request, 'login.html')

# Cadastro
def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se o usuário já está cadastrado
        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Já existe um usuário com esse email.')
            return render(request, 'cadastro.html')

        #Criar um cliente 
        try:
            Cliente.objects.create(nome=nome, email=email, senha=senha)
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
        except:
            messages.error(request, 'Erro ao cadastrar usuário.')
        return redirect('login')

    return render(request, 'cadastro.html')

def principal(request):
    return render(request, 'principal.html')

def deslogar(request):
    del request.session['cliente_id']
    return redirect('login')
