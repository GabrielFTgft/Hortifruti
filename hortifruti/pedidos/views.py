from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Pedido

def ver_pedido(request):
    pedido = Pedido.objects.filter(cliente=request.user, finalizado=False).first()
    if not pedido:
        return render(request, '')  # Caso não haja pedido em aberto

    return render(request, 'ver_pedido.html', {'pedido': pedido})
