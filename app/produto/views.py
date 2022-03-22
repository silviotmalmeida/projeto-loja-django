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
    paginate_by = 6

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'produtos'


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
            messages.error(self.request, 'É necessário o preenchimento dos dados do usuário!')
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


# definindo a view loadtestdata
# tem a função de carregar uma massa de dados de teste
class LoadTestData(View):

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

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

            # sorteando a quantidade de variações a serem criadas
            qtd_variacoes = randint(0, 5)

            # criando as variações
            for x in range(qtd_variacoes):

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

        # criando os usuários
        for x in range(25):
            # cadastrando o novo usuário
            user = User.objects.create_user(
                first_name=f'Nome {x+1}',
                last_name=f'Sobrenome {x+1}',
                username=f'usuario{x+1}',
                password=f'123456',
                email=f'usuario{x+1}@email.com',
            )

            # obtendo um cpf
            cpf = gera_cpf()

            # obtendo um cep
            cep = gera_cep()

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
                logradouro=f'Rua do usuário {x+1}',
                numero=f'Número do usuário {x+1}',
                complemento=f'Complemento do usuário {x+1}',
                bairro=f'Bairro do usuário {x+1}',
                cep=cep,
                cidade=f'Cidade do usuário {x+1}',
                estado=state,
            )

        # redirecionando para a página de início
        return redirect('produto:list')
