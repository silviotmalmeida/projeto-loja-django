# importação default
from django.shortcuts import render

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View


# definindo a view List
class List(ListView):
    pass

# definindo a view Detail
class Detail(View):
    pass

# definindo a view AddCart
class AddCart(View):
    pass

# definindo a view RemoveCart
class RemoveCart(View):
    pass

# definindo a view ShowCart
class ShowCart(View):
    pass

# definindo a view Finalize
class Finalize(View):
    pass



# definindo a view loadtestdata
# tem a função de carregar uma massa de dados de teste
def loadtestdata(request):
    pass
