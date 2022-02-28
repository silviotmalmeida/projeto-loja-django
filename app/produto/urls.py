# importação default
from django.urls import path

# importando as views do app
from . import views


# definindo o nome do produto como namespace
app_name = 'produto'

# definindo os endpoints do app
urlpatterns = [
    # definindo o endpoint de listagem de produtos
    path('', views.List.as_view(), name='list'),
    # definindo o endpoint de detalhe do produto
    path('<slug>', views.Detail.as_view(), name='detail'),
    # definindo o endpoint de adicionar produto ao carrinho
    path('addcart/', views.AddCart.as_view(), name='addcart'),
    # definindo o endpoint de remover produto do carrinho
    path('removecart/', views.RemoveCart.as_view(), name='removecart'),
    # definindo o endpoint de exibir o carrinho
    path('showcart/', views.ShowCart.as_view(), name='showcart'),
    # definindo o endpoint de finalizar a compra
    path('finalize/', views.Finalize.as_view(), name='finalize'),

    # definindo a url para carregamento de dados de teste
    path('loadtestdata', views.loadtestdata, name='loadtestdata'),
]
