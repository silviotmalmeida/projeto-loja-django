# importando a biblioteca para checagem de números
from .check_numbers import is_number


# método de validação de CEP
def valida_cep(cep):

    # validando a entrada
    # se o tamanho for diferente de 5
    if len(cep) != 5:
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
