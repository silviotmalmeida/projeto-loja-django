# importando o módulo de expressões regulares
import re


# função que verifica se o valor é um float
def is_float(val):
    if isinstance(val, float):
        return True
    if re.search(r'^\-{,1}[0-9]+\.{1}[0-9]+$', val):
        return True

    return False


# função que verifica se o valor é um int
def is_int(val):
    if isinstance(val, int):
        return True
    if re.search(r'^\-{,1}[0-9]+$', val):
        return True

    return False


# função que verifica se o valor é um número válido
def is_number(val):
    return is_int(val) or is_float(val)


# função que recebe uma string e retorna somente os números
def only_numbers(val):
    return re.sub(r'[^0-9]', '', val)


# função que verifica se a string passada é uma repetição de um único caractere
def is_sequence(val):
    if val[0] * len(val) == val:
        return True
    else:
        return False


# função que verifica se a string passada possui um tamanho específico
def exact_lenght(val, lenght:int):

    if len(val) == lenght:
        return True
    else:
        return False