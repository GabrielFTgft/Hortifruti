from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Produto
from django.contrib import messages

def produtos(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('login')

    produtos = Produto.objects.all()
    template = loader.get_template('produtos.html')
    context = {
        'produtos': produtos,
    }
    return HttpResponse(template.render(context, request))