# importação default
from django.shortcuts import render, redirect, reverse

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

# importando a model Pedido e ItemPedido
from .models import Pedido, ItemPedido

# importando a model Variacao
from produto.models import Variacao

# importando as mensagens do django
from django.contrib import messages

# importação biblioteca de funções genéricas
from utils import utils


# criando middleware para verificar se o usuário está logado
# e filtrar as consultas por este usuário logado
class DispatchLoginRequiredMixin(View):
    # customizando o método dispatch
    def dispatch(self, *args, **kwargs):

        # se o usuário não estiver logado
        if not self.request.user.is_authenticated:
            # redireciona para a página de login
            return redirect('perfil:create')

        # retornando a classe
        return super().dispatch(*args, **kwargs)

    # customizando a query padrão
    def get_queryset(self, *args, **kwargs):

        # herdando o comportamento padrão
        qs = super().get_queryset(*args, **kwargs)

        # filtrando os resultados pelo usuário logado
        qs = qs.filter(id_usuario=self.request.user)

        # retornando a query customizada
        return qs


# definindo a view Pay
# só terá acesso a página usuários logados
# os reultados serão filtrados para este usuário logado
class Pay(DispatchLoginRequiredMixin, DetailView):

    # definindo o template a ser utilizado
    template_name = 'pedido/pay.html'

    # definindo a model a ser utilizada
    model = Pedido

    # determinando o termo a ser considerado como id na definição da url
    pk_url_kwarg = 'pk'

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'pedido'


# definindo a view Save
class Save(View):

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # se o usuário não estiver logado
        if not self.request.user.is_authenticated:

            # envia mensagem de erro
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )

            # redireciona para a página de login
            return redirect('perfil:create')

        # se não existir o carrinho da sessão
        if not self.request.session.get('cart'):

            # envia mensagem de erro
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )

            # redireciona para a home
            return redirect('produto:list')

        # obtendo o carrinho da sessão
        cart = self.request.session.get('cart')

        # obtendo os id das variações presentes no carrinho
        cart_variacao_ids = [v for v in cart]

        # obtendo os dados atuais das respectivas variações no bd
        # a clausula select_related otimiza o número de consultas ao bd
        bd_variacoes = list(
            Variacao.objects.select_related('id_produto')
            .filter(id__in=cart_variacao_ids)
        )

        # iterando sobre o array de variações
        for variacao in bd_variacoes:

            # obtendo o id da variação da iteração atual
            vid = str(variacao.id)

            # obtendo a quantidade inserida no carrinho
            qtd_cart = cart[vid]['qtd']

            # obtendo o preço no carrinho
            price_cart = cart[vid]['preco_unitario']

            # obtendo o preço promocional no carrinho
            promotion_price_cart = cart[vid]['preco_unitario_promocional']

            # inicializando a flag de alteração do carrinho
            refresh_cart = False

            # se o preço estiver diferente
            if variacao.preco != price_cart:

                # ajusta os preços
                cart[vid]['preco_unitario'] = variacao.preco
                cart[vid]['preco_total'] = qtd_cart * variacao.preco

                # atualizando a variável
                price_cart = cart[vid]['preco_unitario']

                # seta a flag de alteração do carrinho
                refresh_cart = True

            # se o preço promocional estiver diferente
            if variacao.preco_promocional != promotion_price_cart:

                # ajusta os preços
                cart[vid]['preco_unitario_promocional'] = variacao.preco_promocional
                cart[vid]['preco_total_promocional'] = qtd_cart * \
                    variacao.preco_promocional

                # atualizando a variável
                promotion_price_cart = cart[vid]['preco_unitario_promocional']

                # seta a flag de alteração do carrinho
                refresh_cart = True

            # se o estoque for insuficiente
            if variacao.estoque < qtd_cart:

                # ajusta a quantidade ao estoque disponível,
                # bem como os preços totalizados no carrinho
                cart[vid]['qtd'] = variacao.estoque
                cart[vid]['preco_total'] = variacao.estoque * price_cart
                cart[vid]['preco_total_promocional'] = variacao.estoque * \
                    promotion_price_cart

                # atualizando a variável
                qtd_cart = cart[vid]['qtd']

                # seta a flag de alteração do carrinho
                refresh_cart = True

        # se houve alterações no carrinho
        if refresh_cart:

            # definindo a mensagem de alteração do carrinho
            error_msg_estoque = 'Houve alteração em alguns itens '\
                'do seu carrinho em virtude de atualização de preços '\
                'e/ou estoque. Favor verifique novamente seu carrinho'

            # exibe a mensagem de alteração
            messages.error(
                self.request,
                error_msg_estoque
            )

            # salva o estado da sessão
            self.request.session.save()

            # redireciona para a página do carrinho
            return redirect('produto:showcart')

        # obtendo a quantidade total de itens no carrinho
        qtd_items_cart = utils.sum_items(cart)

        # obtendo o valor total dos itens no carrinho
        price_total_cart = round(utils.sum_prices(cart), 2)

        # criando o objeto Pedido com os dados do carrinho
        pedido = Pedido.objects.create(
            id_usuario=self.request.user,
            total=price_total_cart,
            quantidade=qtd_items_cart,
            status='C',
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

        # HACK
        # # passo para decremento do estoque disponível
        # # iterando sobre o array de variações para atualização do estoque no bd
        # for variacao in bd_variacoes:

        #     # obtendo o id da variação da iteração atual
        #     vid = str(variacao.id)

        #     # obtendo a quantidade inserida no carrinho
        #     qtd_cart = cart[vid]['qtd']

        #     # atualizando o estoque
        #     variacao.estoque = variacao.estoque - qtd_cart

        # # atualizando os registros em lote no bd
        # Variacao.objects.bulk_update(bd_variacoes, fields = ['estoque'])

        # apagando o carrinho da sessão
        del self.request.session['cart']

        # salvando a sessão
        self.request.session.save()

        # redireciona para a página do pedido
        return redirect(
            # construindo a url para a página do pedido
            reverse(
                'pedido:pay',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


# definindo a view List
# só terá acesso a página usuários logados
# os resultados serão filtrados para este usuário logado
class List(DispatchLoginRequiredMixin, ListView):

    # definindo o template a ser utilizado
    template_name = 'pedido/list.html'

    # definindo a model a ser utilizada
    model = Pedido

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'pedidos'

    # definindo a quantidade de itens por página
    paginate_by = 10

    # ordenando os resultados pelo id de forma decrescente
    ordering = ['-id']


# definindo a view Detail
# só terá acesso a página usuários logados
# os resultados serão filtrados para este usuário logado
class Detail(DispatchLoginRequiredMixin, DetailView):
    
    # definindo o template a ser utilizado
    template_name = 'pedido/detail.html'

    # definindo a model a ser utilizada
    model = Pedido

    # determinando o termo a ser considerado como id na definição da url
    pk_url_kwarg = 'pk'

    # determinando o nome do objeto a ser passado ao template
    context_object_name = 'pedido'