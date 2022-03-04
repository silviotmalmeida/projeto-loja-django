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
