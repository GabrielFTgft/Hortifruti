from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Pedido
from django.shortcuts import redirect, get_object_or_404
from produtos.models import Produto
from .models import Pedido, ItemPedido
from django.contrib import messages

def adicionar_ao_carrinho(request, produto_id):
    # Obtém o cliente logado
    cliente_id = request.session.get('cliente_id')  
    if not cliente_id:
        messages.error(request, 'Você precisa estar logado para adicionar itens ao carrinho.')
        return redirect('login')

    # Obtém ou cria o pedido em aberto
    pedido_id = request.session.get('pedido_id')  
    if pedido_id:
        pedido = Pedido.objects.filter(id=pedido_id, cliente_id=cliente_id, finalizado=False).first()
    else:
        pedido = Pedido.objects.create(cliente_id=cliente_id, finalizado=False)
        request.session['pedido_id'] = pedido.id

    if not pedido:
        messages.error(request, 'Erro ao localizar ou criar o pedido.')
        return redirect('produtos')

    # Obtém o produto
    produto = get_object_or_404(Produto, id=produto_id)

    # Obtém a quantidade do formulário
    quantidade = int(request.POST.get('quantidade', 1))

    if quantidade <= 0:
        messages.error(request, 'Quantidade inválida.')
        return redirect('produtos')

    # Verifica se o produto já está no carrinho
    item, criado = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)

    if not criado:
        # Caso o item já exista, aumenta a quantidade
        item.quantidade += quantidade
    else:
        # Se for um item novo, define a quantidade inicial
        item.quantidade = quantidade

    # Salva o item no banco
    item.save()

    messages.success(request, f'{produto.nome} foi adicionado ao carrinho.')
    return redirect('produtos')  # Redireciona de volta para a página de produtos
