# importação default
from django.shortcuts import render

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View

# importando a model Produto
from .models import Produto

# biblioteca de números aleatórios
import random


# definindo a view List
class List(ListView):
    # atribuindo a model a ser utilizada
    model = Produto

    # atribuindo o template a ser utilizado
    template_name = 'produto/list.html'

    # definindo a quantidade de itens por página
    paginate_by = 6

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'produtos'

    # # sobreescrevendo o método do django de criação do contexto
    # def get_context_data(self, **kwargs):

    #     # obtendo o contexto padrão da superclasse
    #     context = super().get_context_data(**kwargs)

    #     # obtendo as categorias cadastradas
    #     categories = Categoria.objects.all()

    #     # adicionando as categorias no contexto do template
    #     context['categories'] = categories

    #     return context

    # # sobreescrevendo a query padrão do django
    # def get_queryset(self):

    #     # chamando o método da superclasse
    #     qs = super().get_queryset()

    #     # incrementando na consulta os dados da categoria para melhorar a performance,
    #     # visto que informações da categoria serão exibidos no template
    #     qs = qs.select_related('id_categoria')

    #     # filtrando por publicado=True e ordenando de forma decrescente por id
    #     qs = qs.order_by('-id').filter(publicado=True)

    #     # criando um campo anotado para calcular os comentários publicados do post
    #     qs = qs.annotate(

    #         # calculando os comentários que o atributo publicado=True
    #         comentarios_publicados=Count(
    #             Case(
    #                 When(comentario__publicado=True, then=1)
    #             )
    #         )
    #     )

    #     # retornando a query
    #     return qs

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

    print("entrei")

    # criando os produtos
    for x in range(50):
        # cadastrando o novo produto
        # produto = Produto.objects.create(
        #     nome=f'Produto {x+1}',
        #     descricao_curta=f'Decrição curta do Produto {x+1}',
        #     descricao_longa=f'Decrição longa do Produto {x+1}',
        #     )
        # produto.save()
        print(x)
