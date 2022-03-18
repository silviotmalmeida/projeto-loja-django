# importando a biblioteca de data
from datetime import datetime, timedelta

# importando o gerador de números aleatórios
from random import random


# método de geração de datas aleatórias
def randomYYYYMMDD(min_year=1915, max_year=2000):

    # obtendo as datas limite, recebidas por argumento
    min_date = datetime(min_year,  1,1)
    max_date = datetime(max_year+1,1,1)

    # sorteando um delta de datas alatório entre as datas limite
    delta = random()*(max_date - min_date).total_seconds()

    # retornando a data no formato YYYY-MM-DD
    return (min_date + timedelta(seconds=delta)).strftime("%Y-%m-%d")