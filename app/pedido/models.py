# importação default
from django.db import models
# importando a model de usuário da área administrativa do django
from django.contrib.auth.models import User
# importando a biblioteca de hora e data
from django.utils import timezone


# criando a model de Pedido
class Pedido(models.Model):

    # criando o atributo id_usuario com referência à model Produto, com deleção em cascata
    id_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')

    # criando o atributo data como datetime atual
    data = models.DateTimeField(default=timezone.now, verbose_name='Data')

    # criando o atributo total como float
    total = models.FloatField(verbose_name='Valor Total (R$)')

    # criando o atributo quantidade como inteiro positivo
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade Total de Itens')

    # criando o atributo status com opções pré-definidas
    status = models.CharField(default='C',
                              max_length=1,
                              choices=(
                                  ('A', 'Aprovado'),
                                  ('C', 'Criado'),
                                  ('R', 'Reprovado'),
                                  ('P', 'Pendente'),
                                  ('E', 'Enviado'),
                                  ('F', 'Finalizado'),
                              ),
                              verbose_name='Status')

    # definindo qual atributo da model será exibido na área administrativa
    def __str__(self):
        return f'Pedido {self.id}'

    # definindo os nomes da model a serem exibidos na área administrativa
    class Meta:
        # nome no singular
        verbose_name = 'Pedido'
        # nome no plural
        verbose_name_plural = 'Pedidos'


# criando a model de Pedido
class ItemPedido(models.Model):

    # criando o atributo id_pedido com referência à model Pedido, com deleção em cascata
    id_pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, verbose_name='Pedido')

    # criando o atributo id_produto como inteiro positivo
    id_produto = models.PositiveIntegerField(verbose_name='ID do Produto')

    # criando o atributo nome_produto como texto com tamanho máximo de 255
    nome_produto = models.CharField(max_length=255, verbose_name='Nome do Produto')

    # criando o atributo id_variacao como inteiro positivo
    id_variacao = models.PositiveIntegerField(verbose_name='ID da Variação do Produto')

    # criando o atributo nome_varicao como texto com tamanho máximo de 50
    nome_variacao = models.CharField(max_length=50, verbose_name='Nome da Variação do Produto')

    # criando o atributo preco como float
    preco = models.FloatField(verbose_name='Preço (R$)')

    # criando o atributo preco_promocional, opcional, como float
    preco_promocional = models.FloatField(
        blank=True, null=True, verbose_name='Preço Promocional (R$)')

    # criando o atributo quantidade como inteiro positivo
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade')

    # criando o atributo imagem como texto com tamanho máximo de 255
    # para armazenar somente o path da imagem utilizada no momento da compra
    imagem = models.CharField(max_length=2000, verbose_name='Caminho da Imagem')

    # definindo qual atributo da model será exibido na área administrativa
    def __str__(self):
        return f'Item {self.id} do {self.id_pedido}'

    # definindo os nomes da model a serem exibidos na área administrativa
    class Meta:
        # nome no singular
        verbose_name = 'Item de pedido'
        # nome no plural
        verbose_name_plural = 'Itens de pedido'