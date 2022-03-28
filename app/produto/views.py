# importação default
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

# importando as mensagens do django
from django.contrib import messages

# importando as models Produto e Variacao
from .models import Produto, Variacao

# importando a model User do django
from django.contrib.auth.models import User

# importando a model Perfil
from perfil.models import Perfil

# importando a model Pedido e ItemPedido
from pedido.models import Pedido, ItemPedido

# importando a biblioteca de queries avançadas do django
from django.db.models import Q

# importação biblioteca de funções genéricas
from utils import utils

# importando as bibliotecas de validação de CPF e CEP
from utils.valida_cpf import gera_cpf
from utils.valida_cep import gera_cep
from utils.date_utils import randomYYYYMMDD

# biblioteca de sorteio aleatório
from random import randint, uniform, choice


# definindo a view List
class List(ListView):
    # atribuindo a model a ser utilizada
    model = Produto

    # atribuindo o template a ser utilizado
    template_name = 'produto/list.html'

    # definindo a quantidade de itens por página
    paginate_by = 3

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'produtos'

    # ordenando os resultados pelo id de forma decrescente
    ordering = ['-id']


# definindo a view Search
class Search(List):

    # sobrescrevendo a queryset padrão da view List
    def get_queryset(self, *args, **kwargs):

        # obtendo o termo de busca a partir da url ou da sessão
        search_term = self.request.GET.get(
            'search_term') or self.request.session['search_term']

        # obtendo a queryset default
        qs = super().get_queryset(*args, **kwargs)

        # se não existir o termo de busca
        if not search_term:
            # retorna a queryset padrão
            return qs

        # atualizando a sessão
        self.request.session['search_term'] = search_term
        self.request.session.save()

        # filtrando os resultados dos produtos
        qs = qs.filter(

            # se os campos contiverem o temo de busca
            Q(nome__icontains=search_term) |
            Q(descricao_curta__icontains=search_term) |
            Q(descricao_longa__icontains=search_term)
        )
        # retorna a queryset customizada
        return qs


# definindo a view Detail
class Detail(DetailView):
    # atribuindo a model a ser utilizada
    model = Produto

    # atribuindo o template a ser utilizado
    template_name = 'produto/detail.html'

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'produto'

    # determinando o termo a ser considerado como slug na definição da url
    slug_url_kwarg = 'slug'


# definindo a view AddCart
class AddCart(View):

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # não será permitida a adição da variação diretamente pela url
        # logo tem como premissa que a resuisição se originará a partir de uma página
        # obtendo a url da página que originou a requisição
        if 'HTTP_REFERER' in self.request.META:
            # se existir, popula a variável
            origin_url = self.request.META['HTTP_REFERER']

        # senão
        else:
            # envia mensagem de erro
            messages.error(self.request, 'Página inválida!')
            # redireciona para a página inicial
            return redirect('produto:list')

        # obtendo o id da variação selecionada a partir da url
        variacao_id = self.request.GET.get('vid')

        # se o id da variação não estiver na requisição
        if not variacao_id:
            # envia mensagem de erro
            messages.error(
                self.request, 'Produto indisponível ou não selecionado!')

            # redireciona para a página que originou a requisição
            return redirect(origin_url)

        # obtendo a variação selecionada, caso não exista retorna um 404
        variacao = get_object_or_404(Variacao, id=variacao_id)

        # obtendo o produto da variacao
        produto = variacao.id_produto

        # obtendo a url da imagem do produto
        image = '/default.png' if not produto.imagem else produto.imagem.name

        if variacao.estoque < 1:
            # envia mensagem de erro
            messages.error(
                self.request, 'Infelizmente o produto selecionado não tem estoque suficiente.')

            # redireciona para a página que originou a requisição
            return redirect(origin_url)

        # se o carrinho da sessão ainda não existir
        if not self.request.session.get('cart'):

            # cria o carrinho vazio na sessão
            self.request.session['cart'] = {}
            self.request.session.save()

        # obtendo o carrinho da sessão
        cart = self.request.session['cart']

        # se já existir variação de mesmo tipo no carrinho
        if variacao_id in cart:

            # obtendo a quantidade presente no carrinho
            qtd_cart = cart[variacao_id]['qtd']
            # incrementando a quantidade
            qtd_cart += 1

            # se não houver estoque suficiente
            if variacao.estoque < qtd_cart:
                # envia mensagem de erro
                messages.error(
                    self.request, f'Estoque insuficiente para inclusão. Foram mantidos {variacao.estoque} no carrinho.')

                # readequa a quantidade ao estoque disponível
                qtd_cart = variacao.estoque

            # atualizando a quantidade e preços no carrinho
            cart[variacao_id]['qtd'] = qtd_cart
            cart[variacao_id]['preco_total'] = variacao.preco * qtd_cart
            if variacao.preco_promocional:
                cart[variacao_id]['preco_total_promocional'] = variacao.preco_promocional * qtd_cart

        # senão
        else:

            # inserindo a variação no carrinho
            cart[variacao_id] = {
                'produto_id': produto.id,
                'produto_nome': produto.nome,
                'variacao_id': variacao.id,
                'variacao_nome': variacao.nome,
                'preco_unitario': variacao.preco,
                'preco_unitario_promocional': variacao.preco_promocional,
                'preco_total': variacao.preco,
                'preco_total_promocional': variacao.preco_promocional,
                'qtd': 1,
                'slug': produto.slug,
                'imagem': image,
            }

        # salvando o status da sessão
        self.request.session.save()

        # envia mensagem de sucesso
        messages.success(
            self.request, 'Produto inserido no carrinho.')

        # redireciona para a página que originou a requisição
        return redirect(origin_url)


# definindo a view RemoveCart
class RemoveCart(View):
    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # não será permitida a remoção da variação diretamente pela url
        # logo tem como premissa que a resuisição se originará a partir de uma página
        # obtendo a url da página que originou a requisição
        if 'HTTP_REFERER' in self.request.META:
            # se existir, popula a variável
            origin_url = self.request.META['HTTP_REFERER']

        # senão
        else:
            # envia mensagem de erro
            messages.error(self.request, 'Página inválida!')
            # redireciona para a página inicial
            return redirect('produto:list')

        # obtendo o id da variação selecionada a partir da url
        variacao_id = self.request.GET.get('vid')

        # se o id da variação não estiver na requisição
        if not variacao_id:
            # redireciona para a página que originou a requisição
            return redirect(origin_url)

        # se o carrinho da sessão não existir
        if not self.request.session.get('cart'):
            # redireciona para a página que originou a requisição
            return redirect(origin_url)

        # se o id da variação não estiver no carrinho da sessão
        if variacao_id not in self.request.session.get('cart'):
            # redireciona para a página que originou a requisição
            return redirect(origin_url)

        # removendo o registro da variação no carrinho da sessão
        del(self.request.session['cart'][variacao_id])

        # salvando o status da sessão
        self.request.session.save()

        # envia mensagem de sucesso
        messages.success(self.request, 'Produto removido do carrinho.')

        # redireciona para a página que originou a requisição
        return redirect(origin_url)


# definindo a view ShowCart
class ShowCart(View):

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # definindo o contexto a ser passado ao template
        context = {

            # obtendo o carrinho da sessão
            'cart': self.request.session.get('cart', {})
        }

        # renderizando o template com o contexto
        return render(self.request, 'produto/cart.html', context)


# definindo a view Summary
class Summary(View):

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # se o usuário não estiver autenticado
        if not self.request.user.is_authenticated:

            # redireciona-o para a página de login
            return redirect('perfil:create')

        # verificando se existe perfil para o usuário logado
        perfil = Perfil.objects.filter(id_usuario=self.request.user).exists()

        # se não existir perfil
        if not perfil:
            # envia mensagem de erro
            messages.error(
                self.request, 'É necessário o preenchimento dos dados do usuário!')
            # redireciona-o para a página de atualização do cadastro
            return redirect('perfil:create')

        if not self.request.session.get('cart'):
            # envia mensagem de erro
            messages.error(self.request, 'Seu carrinho está vazio!')
            # redireciona-o para a página de carrinho
            return redirect('produto:showcart')

        # definindo o contexto a ser passado ao template
        context = {

            # obtendo o usuário da sessão
            'user': self.request.user,
            # obtendo o carrinho da sessão
            'cart': self.request.session.get('cart', {})
        }

        # renderizando o template com o contexto
        return render(self.request, 'produto/summary.html', context)


# definindo o método loadtestdata
# tem a função de carregar uma massa de dados de teste
def loadtestdata(request):

    # obtendo todos os produtos cadastrados
    produtos = Produto.objects.all()

    # se não existirem produtos cadastrados
    if not produtos:

        # criando os produtos
        for x in range(50):
            # cadastrando o novo produto
            produto = Produto.objects.create(
                nome=f'Produto {x+1}',
                descricao_curta=f'Descrição curta do Produto {x+1}',
                descricao_longa=f'Descrição longa do Produto {x+1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            )

        # obtendo todos os produtos cadastrados
        produtos = Produto.objects.all()

        # iterando no array de produtos
        for produto in produtos:

            # criando as variações
            for x in range(randint(0, 5)):

                # sorteando se existirá promoção
                if randint(0, 1):
                    preco_promocional = round(uniform(10, 500), 2)
                else:
                    preco_promocional = None

                # cadastrando a nova variação
                variacao = Variacao.objects.create(
                    id_produto=produto,
                    nome=f'Variacao {x+1} {produto.nome}',
                    preco=round(uniform(10, 500), 2),
                    preco_promocional=preco_promocional,
                    estoque=randint(0, 100),)

        # obtendo todos as variações cadastradas
        variacoes = Variacao.objects.all()

        # criando os usuários
        for u in range(25):
            # cadastrando o novo usuário
            user = User.objects.create_user(
                first_name=f'Nome {u+1}',
                last_name=f'Sobrenome {u+1}',
                username=f'usuario{u+1}',
                password=f'123456',
                email=f'usuario{u+1}@email.com',
            )

            # obtendo um cpf
            cpf = gera_cpf()

            # obtendo um cep
            cep = gera_cep()

            # obtendo um número aleatório
            numero = randint(0, 999)

            # obtendo um estado através de sorteio aleatório
            states = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                      'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                      'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
                      ]
            state = choice(states)

            # obtendo data de nascimento aleatória
            birth_date = randomYYYYMMDD()

            # cadastrando o perfil do novo usuário
            perfil = Perfil.objects.create(
                id_usuario=user,
                data_nascimento=birth_date,
                cpf=cpf,
                logradouro=f'Rua do usuário {u+1}',
                numero=numero,
                complemento=f'Complemento do usuário {u+1}',
                bairro=f'Bairro do usuário {u+1}',
                cep=cep,
                cidade=f'Cidade do usuário {u+1}',
                estado=state,
            )

            # criando os carrinhos
            for y in range(randint(0, 20)):

                # inicializando o carrinho vazio
                cart = {}

                # obtendo as variações a serem inseridas no carrinho
                for z in range(randint(1, 5)):

                    # sorteando uma variação
                    variacao = choice(variacoes)

                    # obtendo o produto da variação sorteada
                    produto = variacao.id_produto

                    # obtendo uma quantidade aleatória
                    qtd = randint(1, 10)

                    # obtendo a url da imagem do produto
                    image = '/default.png' if not produto.imagem else produto.imagem.name

                    # inserindo a variação no carrinho
                    # se já existir variação de mesmo tipo no carrinho
                    if variacao.id in cart:

                        # obtendo a quantidade presente no carrinho
                        qtd_cart = cart[variacao.id]['qtd']
                        # incrementando a quantidade
                        qtd_cart += qtd

                        # atualizando a quantidade e preços no carrinho
                        cart[variacao.id]['qtd'] = qtd_cart
                        cart[variacao.id]['preco_total'] = round(
                            variacao.preco * qtd_cart, 2)
                        if variacao.preco_promocional:
                            cart[variacao.id]['preco_total_promocional'] = round(
                                variacao.preco_promocional * qtd_cart, 2)

                    # senão
                    else:

                        # calculando o preço total
                        preco_total = round(variacao.preco * qtd, 2)

                        # se existir preço promocional
                        if variacao.preco_promocional:
                            # calculando o preço total promocional
                            preco_total_promocional = round(
                                variacao.preco_promocional * qtd, 2)
                        # senão
                        else:
                            # deixa o valor original
                            preco_total_promocional = variacao.preco_promocional

                        # inserindo a variação no carrinho
                        cart[variacao.id] = {
                            'produto_id': produto.id,
                            'produto_nome': produto.nome,
                            'variacao_id': variacao.id,
                            'variacao_nome': variacao.nome,
                            'preco_unitario': variacao.preco,
                            'preco_unitario_promocional': variacao.preco_promocional,
                            'preco_total': preco_total,
                            'preco_total_promocional': preco_total_promocional,
                            'qtd': qtd,
                            'imagem': image,
                        }

                # obtendo a quantidade total de itens no carrinho
                qtd_items_cart = utils.sum_items(cart)

                # obtendo o valor total dos itens no carrinho
                price_total_cart = round(utils.sum_prices(cart), 2)

                # obtendo um status através de sorteio aleatório
                status_list = ['A', 'C', 'R', 'P', 'E', 'F']
                status = choice(status_list)

                # criando o objeto Pedido com os dados do carrinho
                pedido = Pedido.objects.create(
                    id_usuario=user,
                    total=price_total_cart,
                    quantidade=qtd_items_cart,
                    status=status,
                )

                # criando os registros dos itens do pedido
                # iterando sobre as variações presentes no carrinho
                ItemPedido.objects.bulk_create(
                    [
                        ItemPedido(
                            id_pedido=pedido,
                            nome_produto=v['produto_nome'],
                            id_produto=v['produto_id'],
                            id_variacao=v['variacao_id'],
                            nome_variacao=v['variacao_nome'],
                            preco=v['preco_unitario'],
                            preco_promocional=v['preco_unitario_promocional'],
                            quantidade=v['qtd'],
                            imagem=v['imagem'],
                        ) for v in cart.values()
                    ]
                )

        # envia mensagem
        messages.success(request, 'Dados de teste carregados!')

    # senão
    else:
        # envia mensagem
        messages.error(request, 'Já existem dados no BD!')

    # redirecionando para a página inicial
    return redirect('produto:list')
