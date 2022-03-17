# arquivo com filtros personalizados criados para a utilização nos templates

# importação default
from django.template import Library
# importação biblioteca de funções genéricas
from utils import utils


# criando o decorador a ser utilizado nos filtros
register = Library()


# criando o filtro reponsável por formatar o preço como moeda
# decorando a função como um filtro chamado currency_format
@register.filter(name='currency_format')
# criando a função
# o argumento a ser recebido é o texto antes do pipe
def currency_format(value):

    return utils.currency_format(value)


# criando o filtro reponsável por somar a quantidade de itens no carrinho
# decorando a função como um filtro chamado sum_items
@register.filter(name='sum_items')
# criando a função
# o argumento a ser recebido é o texto antes do pipe
def sum_items(value):

    return utils.sum_items(value)


# criando o filtro reponsável por somar o preço de itens no carrinho
# decorando a função como um filtro chamado sum_prices
@register.filter(name='sum_prices')
# criando a função
# o argumento a ser recebido é o texto antes do pipe
def sum_prices(value):

    return utils.sum_prices(value)


# criando o filtro reponsável por obter a idade do usuário
# decorando a função como um filtro chamado age
@register.filter(name='age')
# criando a função
# o argumento a ser recebido é o texto antes do pipe
def age(value):

    return utils.age(value)
