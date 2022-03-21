# importação default
from django.shortcuts import render, redirect

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View

# importando a model Variacao
from produto.models import Variacao

# importando as mensagens do django
from django.contrib import messages


# definindo a view Pay
class Pay(View):
    pass


# definindo a view Save
class Save(View):

    # atribuindo o template a ser utilizado
    template_name = 'pedido/pay.html'

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
        bd_variacoes = list(
            Variacao.objects.select_related('id_produto')
            .filter(id__in=cart_variacao_ids)
        )

        # iterando sobre o array de variações
        for variacao in bd_variacoes:

            # obtendo o id da variação da iteração atual
            vid = str(variacao.id)

            # obtendo o estoque disponível
            estoque = variacao.estoque

            # obtendo a quantidade inserida no carrinho
            qtd_cart = cart[vid]['quantidade']

            # obtendo o preço no carrinho
            preco_unt = cart[vid]['preco_unitario']

            # obtendo o preço promocional no carrinho
            preco_unt_promo = cart[vid]['preco_unitario_promocional']

            # inicializando a flag de alteração do carrinho
            refresh_cart = False

            # se o estoque for insuficiente
            if variacao.estoque < qtd_cart:

                # ajusta a quantidade ao estoque disponível,
                # bem como os preços totalizadosno carrinho
                cart[vid]['quantidade'] = estoque
                cart[vid]['preco_quantitativo'] = estoque * preco_unt
                cart[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                # seta a flag de alteração do carrinho
                refresh_cart = True

            # se o estoque for insuficiente
            if estoque < qtd_cart:

                # ajusta a quantidade ao estoque disponível,
                # bem como os preços totalizadosno carrinho
                cart[vid]['quantidade'] = estoque
                cart[vid]['preco_quantitativo'] = estoque * preco_unt
                cart[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                # seta a flag de alteração do carrinho
                refresh_cart = True
                

        # se houve alterações no carrinho
        if refresh_cart:

            # definindo a mensagem de alteração do carrinho
            error_msg_estoque = 'Houve alteração em alguns itens '\
                    'do carrinho em virtude de atualização de preços '\
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

        # qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        # valor_total_carrinho = utils.cart_totals(carrinho)

        # pedido = Pedido(
        #     usuario=self.request.user,
        #     total=valor_total_carrinho,
        #     qtd_total=qtd_total_carrinho,
        #     status='C',
        # )

        # pedido.save()

        # ItemPedido.objects.bulk_create(
        #     [
        #         ItemPedido(
        #             pedido=pedido,
        #             produto=v['produto_nome'],
        #             produto_id=v['produto_id'],
        #             variacao=v['variacao_nome'],
        #             variacao_id=v['variacao_id'],
        #             preco=v['preco_quantitativo'],
        #             preco_promocional=v['preco_quantitativo_promocional'],
        #             quantidade=v['quantidade'],
        #             imagem=v['imagem'],
        #         ) for v in carrinho.values()
        #     ]
        # )

        # del self.request.session['carrinho']

        # return redirect(
        #     reverse(
        #         'pedido:pagar',
        #         kwargs={
        #             'pk': pedido.pk
        #         }
        #     )
        # )
        return redirect('perfil:create')


# definindo a view Detail
class Detail(View):
    pass
