from django.db import models
from usuarios.models import Cliente
from produtos.models import Produto

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente que fez o pedido
    criado_em = models.DateTimeField(auto_now_add=True)  # Data do pedido
    finalizado = models.BooleanField(default=False)  # Status do pedido (em aberto ou finalizado)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')  # Pedido associado
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Produto associado
    quantidade = models.PositiveIntegerField()  # Quantidade do produto no pedido

    def __str__(self):
        return f"{self.quantidade} - {self.produto.nome} - {self.pedido.id}"
