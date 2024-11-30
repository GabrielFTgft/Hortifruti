from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()

    def __str__(self):
        return self.nome
