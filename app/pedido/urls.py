# importação default
from django.urls import path

# importando as views do app
from . import views


# definindo o nome do pedido como namespace
app_name = 'pedido'

# definindo os endpoints do app
urlpatterns = [
    # definindo o endpoint de pagamento de pedidos
    path('', views.Pay.as_view(), name='pay'),
    # definindo o endpoint de fechamento de pedidos
    path('close/', views.Close.as_view(), name='close'),
    # definindo o endpoint de detalhe de pedidos
    path('detail/', views.Detail.as_view(), name='login'),
]
