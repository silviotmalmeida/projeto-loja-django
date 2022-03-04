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
