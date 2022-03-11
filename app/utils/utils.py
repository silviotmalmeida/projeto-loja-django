# funções genéricas


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
