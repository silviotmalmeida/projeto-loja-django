# funções genéricas

# importando a biblioteca de datas
from datetime import date


# função reponsável por formatar o preço como moeda
def currency_format(value):

    # tratando exceções
    try:

        # obtendo o valor em float
        value = float(value)

        # retorna o valor formatado
        return f'R$ {value:.2f}'.replace('.', ',')

    # em caso de exceção
    except:
        # retorna o valor original
        return value


# função reponsável por somar a quantidade de itens no carrinho
def sum_items(cart):

    # somando a quantidade de itens utilizando list comprehension
    # somando os valores presentes no atributo qtd de cada item do carrinho
    return sum([item['qtd'] for item in cart.values()])


# função reponsável por somar o preço total de itens no carrinho
def sum_prices(cart):

    # somando o preço total de itens utilizando list comprehension
    # somando os preços totais de cada item do carrinho
    # se existir preço_total_promocional, usa-o
    # senão usa o preço_total
    return sum(
        [
            item.get('preco_total_promocional')
            if item.get('preco_total_promocional')
            else item.get('preco_total')
            for item
            in cart.values()
        ]
    )


# função que calcula a idade atual a partir da data de nascimento
def age(birth_date):
    # obtendo a data de hoje
    today = date.today()

    # calculando a diferença dos anos
    age = today.year - birth_date.year

    # se o mes atual e o dia atual são inferiores ao de nascimento
    if today.month < birth_date.month and today.day < birth_date.day:
        # decrementa a idade em 1
        age -= 1

    # retorna a idade calculada
    return age
