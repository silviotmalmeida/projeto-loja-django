# importação default
from django.shortcuts import render

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View


# definindo a view Pay
class Pay(View):
    pass


# definindo a view Save
class Save(View):

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # renderizando o template com o contexto
        return render(self.request, 'pedido/save.html')


# definindo a view Detail
class Detail(View):
    pass
