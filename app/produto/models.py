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

    # criando o atributo preco_marketing como float
    preco_marketing = models.FloatField(verbose_name='Preço (R$)')

    # criando o atributo preco_marketing_promocional, opcional, como float
    preco_marketing_promocional = models.FloatField(
        blank=True, null=True, verbose_name='Preço Promocional (R$)')

    # criando o atributo tipo com opções pré-definidas
    tipo = models.CharField(default='V',
                            max_length=1,
                            choices=(
                                ('V', 'Variável'),
                                ('S', 'Simples'),
                            ),
                            verbose_name='Tipo')

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
        return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')
    formatted_preco_marketing.short_description = 'Preço (R$)'

    # definindo função para exibir o preco_marketing_promocional formatado na listagem
    def formatted_preco_marketing_promocional(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')
    formatted_preco_marketing_promocional.short_description = 'Preço Promocional (R$)'

    # sobrescrevendo o método do django de salvar no BD
    def save(self, *args, **kwargs):

        # obtendo as variaçoes cadastradas
        variacoes = Variacao.objects.filter(id_produto=self)

        if (variacoes):

            self.tipo = 'V'

            lower_price = 100000.00
            lower_price_promotional = 100000.00
            for variacao in variacoes:

                print(variacao.preco_marketing)

                if(variacao.preco_marketing < lower_price):
                    lower_price = variacao.preco_marketing
                    lower_price_promotional = variacao.preco_marketing_promocional

            self.preco_marketing = lower_price
            self.preco_marketing_promocional = lower_price_promotional

        else:

            self.tipo = 'S'

            # se o preco_marketing_promocional não foi informado
            if not self.preco_marketing_promocional:
                # atribui o mesmo valor do preco_marketing
                self.preco_marketing_promocional = self.preco_marketing

        # se o slug não foi informado
        if not self.slug:
            # cria um slug com o nome e um número aleatório
            slug = f'{slugify(self.nome)}-{random.randint(1, 100)}'
            # atribuindo o slug
            self.slug = slug

        # utilizando as definições da superclasse
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

    # criando o atributo nome como texto, opcional, com tamanho máximo de 50
    nome = models.CharField(max_length=50, blank=True,
                            null=True, verbose_name='Nome')

    # criando o atributo preco_marketing como float
    preco_marketing = models.FloatField(verbose_name='Preço (R$)')

    # criando o atributo preco_marketing_promocional, opcional, como float
    preco_marketing_promocional = models.FloatField(
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

        # se o preco_marketing_promocional não foi informado
        if not self.preco_marketing_promocional:
            # atribui o mesmo valor do preco_marketing
            self.preco_marketing_promocional = self.preco_marketing



        # obtendo as variaçoes cadastradas
        produto = self.id_produto

        print(produto.preco_marketing)
        print(produto.preco_marketing_promocional)

        if(self.preco_marketing < produto.preco_marketing):
     
            produto.preco_marketing = self.preco_marketing
            produto.preco_marketing_promocional = self.preco_marketing_promocional

        print(produto.preco_marketing)
        print(produto.preco_marketing_promocional)

        produto.save()


        # utilizando as definições da superclasse
        super().save(*args, **kwargs)

