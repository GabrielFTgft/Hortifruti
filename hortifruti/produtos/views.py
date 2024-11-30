from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Produto

def produtos(request):
    produtos = Produto.objects.all()
    template = loader.get_template('produtos.html')
    context = {
        'produtos': produtos,
    }
    return HttpResponse(template.render(context, request))