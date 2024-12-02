from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Pedido
from .models import ItemPedido

admin.site.register(Pedido)
admin.site.register(ItemPedido)