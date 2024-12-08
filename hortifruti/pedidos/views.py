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

def mostrar_carrinho(request):
    cliente_id = request.session.get('cliente_id')  
    if not cliente_id:
        messages.error(request, 'Você precisa estar logado para adicionar itens ao carrinho.')
        return redirect('login')

    # pedido_id = request.session.get('pedido_id')  
    pedido_id = 1
    if pedido_id:
        pedido = Pedido.objects.filter(id=pedido_id, finalizado=False).first()
    else:
        return
        # return render(request, "carrinho.html")
    
    itens_pedido = ItemPedido.objects.filter(pedido=pedido)
    total = 0
    for item in itens_pedido:
        item.total = round(item.quantidade * item.produto.preco, 2)
        total += item.total
    total = round(total, 2)

    template = loader.get_template('carrinho.html')
    context = {
        'itensPedido': itens_pedido,
        'total':total,
    }
    return HttpResponse(template.render(context, request))

#@csrf_exempt 
def alterar_item_carrinho(request, item_id, quantidade):
    item_pedido = get_object_or_404(ItemPedido, id=item_id)
    if request.method == "PUT":
        quantity = quantidade
        # quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item_pedido.quantidade = quantity
            item_pedido.save()
        else:
            item_pedido.delete()  # Remove o item se a quantidade for 0
    return redirect("carrinho")

def deletar_item_carrinho(request, item_id):
    item_pedido = get_object_or_404(ItemPedido, id=item_id)
    item_pedido.delete()
    return redirect("carrinho")

def finalizar_ordem(request):
    if request.method == "POST":
        pedido_id = request.session.get('pedido_id')  
        if pedido_id:
            pedido = Pedido.objects.filter(id=pedido_id, finalizado=False).first()
            pedido.finalizado = True
            pedido.save()   
            del request.session['pedido_id']
        return redirect('produtos')
        
