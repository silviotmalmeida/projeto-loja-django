# importação default
from django.db import models


# criando a model de Produto
class Produto(models.Model):

    # TODO

    # criando o atributo nome como texto com tamanho máximo de 255
    nome = models.CharField(max_length=255, verbose_name='Nome')

    # criando o atributo descricao_curta como texto
    descricao_curta = models.TextField(
        max_length=255, verbose_name='Descrição Curta')

    # criando o atributo descricao_longa como texto
    descricao_longa = models.TextField(verbose_name='Descrição Longa')

    # criando o atributo imagem, opcional, e definindo o destino do arquivo
    imagem = models.ImageField(
        blank=True, null=True, upload_to='pictures/%Y/%m/', verbose_name='Imagem')

    # criando o atributo slug como texto único
    # atributo para definir um apelido amigável
    slug = models.SlugField(unique=True, verbose_name='Apelido')

    # criando o atributo preco_marketing como float
    preco_marketing = models.FloatField(verbose_name='Preço')

    # criando o atributo preco_marketing_promocional, opcional, como float
    preco_marketing_promocional = models.FloatField(
        blank=True, null=True, verbose_name='Preço Promocional')

    # criando o atributo tipo com opções pré-definidas
    tipo = models.CharField(default='V',
                            max_length=1,
                            choices=(
                                ('V', 'Variação'),
                                ('S', 'Simples'),
                            ))

    # definindo qual atributo da model será exibido na área administrativa
    def __str__(self):
        return self.titulo
