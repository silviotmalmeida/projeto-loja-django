# importação default
from django.shortcuts import render, redirect

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View

# importando as models Produto e Variacao
from .models import Produto, Variacao

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

    # criando os produtos
    for x in range(50):
        # cadastrando o novo produto
        produto = Produto.objects.create(
            nome=f'Produto {x+1}',
            descricao_curta=f'Descrição curta do Produto {x+1}',
            descricao_longa=f'Descrição longa do Produto {x+1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            preco_marketing=round(random.uniform(10, 500), 2),
            preco_marketing_promocional=round(random.uniform(10, 500), 2),)

    # obtendo todos os produtos cadastrados
    produtos = Produto.objects.all()

    # iterando no array de produtos
    for produto in produtos:

        # sorteando a quantidade de variações a serem criadas
        qtd_variacoes = random.randint(0, 5)

        # criando as variações
        for x in range(qtd_variacoes):
            # cadastrando a nova variação
            variacao = Variacao.objects.create(
                id_produto=produto,
                nome=f'Variacao {x+1} {produto.nome}',
                preco=round(random.uniform(10, 500), 2),
                preco_promocional=round(random.uniform(10, 500), 2),
                estoque=random.randint(0, 100),)

    # redirecionando para a página de início
    return redirect('list')
