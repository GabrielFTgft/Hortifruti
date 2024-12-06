from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nome}"
