from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto

class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)  # Cliente que fez o pedido
    criado_em = models.DateTimeField(auto_now_add=True)  # Data do pedido
    atualizado_em = models.DateTimeField(auto_now=True)  # Última atualização
    finalizado = models.BooleanField(default=False)  # Status do pedido (em aberto ou finalizado)

    def __str__(self):
        return self.id

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')  # Pedido associado
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Produto associado
    quantidade = models.PositiveIntegerField()  # Quantidade do produto no pedido

    def __str__(self):
        return f"{self.quantidade} - {self.produto.nome} - {self.pedido.id}"
