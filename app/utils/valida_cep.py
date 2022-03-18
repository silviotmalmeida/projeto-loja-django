# importando a biblioteca para checagem de números
from .check_numbers import is_number

# importando o gerador de números aleatórios
from random import randint


# método de geração de CEP
def gera_cep():

    # laço para gerar aleatoriamente os oito dígitos do cep
    while True:
        # obtendo os oito dígitos do CEP
        # inicializando o cep vazio
        cep = ''

        # laço para popular os oito dígitos
        for x in range(8):
            # populando aleatoriamente os oito dígitos
            cep += str(randint(0, 9))

        # se nao for repetição
        if not cep == (cep[0] * 8):
            # sai do laço
            break

    # envia o CEP gerado
    return cep


# método de validação de CEP
def valida_cep(cep):

    # validando a entrada
    # se o tamanho for diferente de 8
    if len(cep) != 8:
        return False

    # se não for número
    if not is_number(cep):
        return False

    # se conter traço
    if '-' in cep:
        return False

    # se conter ponto
    if '.' in cep:
        return False

    # se for repetição
    if cep == (cep[0] * 11):
        return False

    # senão retorna True
    return True
