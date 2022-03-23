# importação default
from django.db import models
# importando o pillow para processamento de imagens
from PIL import Image
# obtendo os dados do app definidos no settings
from django.conf import settings
# importando a biblioteca de navegação de arquivos
import os
# importando a biblioteca de criação de slugs
from django.utils.text import slugify
# biblioteca de números aleatórios
import random
# importação biblioteca de funções genéricas
from utils import utils


# criando a model de Produto
class Produto(models.Model):

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
    slug = models.SlugField(unique=True, blank=True,
                            null=True, verbose_name='Slug')

    # criando o atributo preco_marketing como float, não editável
    preco_marketing = models.FloatField(
        blank=True, null=True, editable=False, verbose_name='Preço (R$)')

    # criando o atributo preco_marketing_promocional como float, não editável
    preco_marketing_promocional = models.FloatField(
        blank=True, null=True, editable=False, verbose_name='Preço Promocional (R$)')

    # criando o atributo disponivel como booleano, com default False, não editável
    disponivel = models.BooleanField(
        default=False, editable=False, verbose_name='Disponível?')

    # definindo qual atributo da model será exibido na área administrativa
    def __str__(self):
        return self.nome

    # definindo os nomes da model a serem exibidos na área administrativa
    class Meta:
        # nome no singular
        verbose_name = 'Produto'
        # nome no plural
        verbose_name_plural = 'Produtos'

    # definindo função para exibir o preco_marketing formatado na listagem
    def formatted_preco_marketing(self):
        return utils.currency_format(self.preco_marketing)
    formatted_preco_marketing.short_description = 'Preço (R$)'

    # definindo função para exibir o preco_marketing_promocional formatado na listagem
    def formatted_preco_marketing_promocional(self):
        return utils.currency_format(self.preco_marketing_promocional)
    formatted_preco_marketing_promocional.short_description = 'Preço Promocional (R$)'

    # sobrescrevendo o método do django de salvar no BD
    def save(self, *args, **kwargs):

        # se o slug não foi informado
        if not self.slug:
            # cria um slug com o nome e um número aleatório
            slug = f'{slugify(self.nome)}-{random.randint(1, 999)}'
            # atribuindo o slug
            self.slug = slug

        # utilizando as definições da superclasse para salvar no BD
        super().save(*args, **kwargs)

        # se existir imagem a ser submetida
        if self.imagem:
            # processando a imagem submetida
            self.resize_image(self.imagem)

    # criando método estático para processamento da imagem do post
    @staticmethod
    def resize_image(image_name, new_width=800):

        # obtendo o caminho da imagem
        img_path = os.path.join(settings.MEDIA_ROOT, str(image_name))

        # obtendo os dados da imagem original
        original_image = Image.open(img_path)
        width, height = original_image.size

        # se o comprimento da imagem for menor ou igual ao novo comprimento
        if width <= new_width:
            # fecha a imagem
            original_image.close()
        else:
            # calculando a nova altura
            new_height = round((new_width * height)/width)
            # criando a nova imagem
            new_image = original_image.resize(
                (new_width, new_height), Image.LANCZOS)
            # salvando a nova imagem otimizada no lugar da original
            new_image.save(img_path, optimize=True, quality=50)
            # fechando a imagem
            new_image.close()


# criando a model de Variacao
class Variacao(models.Model):

    # criando o atributo id_produto com referência à model Produto, com deleção em cascata
    id_produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, verbose_name='Produto')

    # criando o atributo nome como texto, com tamanho máximo de 50
    nome = models.CharField(max_length=50, verbose_name='Nome')

    # criando o atributo preco como float
    preco = models.FloatField(verbose_name='Preço (R$)')

    # criando o atributo preco_promocional como float, opcional
    preco_promocional = models.FloatField(
        blank=True, null=True, verbose_name='Preço Promocional (R$)')

    # criando o atributo estoque como inteiro positivo
    estoque = models.PositiveIntegerField(default=0, verbose_name='Estoque')

    # definindo qual atributo da model será exibido na área administrativa
    # caso o nome da variação seja nulo, exibe o nome do produto
    def __str__(self):
        return self.nome or self.id_produto.nome

    # definindo os nomes da model a serem exibidos na área administrativa
    class Meta:
        # nome no singular
        verbose_name = 'Variação'
        # nome no plural
        verbose_name_plural = 'Variações'

    # sobrescrevendo o método do django de salvar no BD
    def save(self, *args, **kwargs):

        # se o nome não foi inserido
        if not self.nome:
            # atribui o mesmo nome do produto
            self.nome = self.id_produto.nome

        # se o preco_promocional for maior que o preco
        if self.preco_promocional and self.preco_promocional > self.preco:
            # remove o preco_promocional
            self.preco_promocional = None

        # utilizando as definições da superclasse para salvar no BD
        super().save(*args, **kwargs)

        # atualizando os preços do produto
        self.refreshProductPrice()

    # sobrescrevendo o método do django de remover do BD
    def delete(self, *args, **kwargs):

        # utilizando as definições da superclasse para remover do BD
        super().delete(*args, **kwargs)

        # atualizando os preços do produto
        self.refreshProductPrice()

    # método para atualização dos preços do produto baseado no menor preço promocional de suas variações
    def refreshProductPrice(self):

        # obtendo os dados do produto relativo à variação
        produto = self.id_produto

        # obtendo as variaçoes cadastradas neste produto
        variacoes = Variacao.objects.filter(id_produto=self.id_produto)

        # se existirem variações
        if (variacoes):

            # define o produto como disponível
            produto.disponivel = True

            # inicializando as variáveis de menor preço
            lower_price = 1000000.00
            lower_price_promotional = 1000000.00

            # iterando no array de variações
            for variacao in variacoes:

                # se o preço da variação for menor que o menor preço
                if(variacao.preco < lower_price):
                    # atualiza as variáveis de menor preço
                    lower_price = variacao.preco
                    lower_price_promotional = variacao.preco_promocional

            # atribui os preços ajustados ao produto
            if lower_price != 1000000.00:
                produto.preco_marketing = lower_price
            if lower_price_promotional != 1000000.00:
                produto.preco_marketing_promocional = lower_price_promotional

        # senão
        else:
            # define o produto como indisponível
            produto.disponivel = False

            # atribui os preços vazios ao produto
            produto.preco_marketing = None
            produto.preco_marketing_promocional = None

        # salva no BD
        produto.save()
