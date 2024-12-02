from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/', views.adicionar_ao_carrinho, name='pedido'),
]
