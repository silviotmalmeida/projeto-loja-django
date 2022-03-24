# importação default
from django.urls import path

# importando as views do app
from . import views


# definindo o nome do pedido como namespace
app_name = 'pedido'

# definindo os endpoints do app
urlpatterns = [
    # definindo o endpoint de pagamento de pedidos
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    # definindo o endpoint de salvamento de pedidos
    path('save/', views.Save.as_view(), name='save'),
    # definindo o endpoint de listagem de pedidos
    path('list/', views.List.as_view(), name='list'),
    # definindo o endpoint de detalhe de pedidos
    path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
]
