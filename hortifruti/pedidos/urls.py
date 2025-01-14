from django.urls import path
from . import views

#app_name = 'pedido'  # Define o namespace do app

urlpatterns = [
    path('carrinho', views.mostrar_carrinho, name='carrinho'),
    path('adicionar/<int:item_id>/<int:quantidade>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/alterar/<int:item_id>/<int:quantidade>/', views.alterar_item_carrinho, name="alterar_item_carrinho"),
    path('carrinho/deletar/<int:item_id>/', views.deletar_item_carrinho, name="deletar_item_carrinho"),
    path('carrinho/finalizar', views.finalizar_ordem, name="finalizar_ordem")
]
