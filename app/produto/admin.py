# importação default
from django.contrib import admin
# importando as models do app
from .models import Produto, Variacao


# definindo as configurações de exibição da Variacao na área administrativa da model Produto
class VariacaoInline(admin.TabularInline):
    # model a ser utilizado
    model = Variacao
    # quantidade de variações em branco a serem exibidas
    extra = 1

# definindo as configurações de exibição do Produto na área administrativa
class ProdutoAdmin(admin.ModelAdmin):

    # definindo as demais models a serem apresentadas
    inlines = [VariacaoInline]

    # definindo as colunas a serem exibidas
    list_display = ('id', 'nome', 'descricao_curta', 'formatted_preco_marketing',
                    'formatted_preco_marketing_promocional', 'disponivel')

    # definindo em quais colunas serão colocados links de edição
    list_display_links = ('id', 'nome')

    # definindo o limite de registros por página
    list_per_page = 10

    # definindo as colunas a serem consideradas no campo de pesquisa
    search_fields = ('nome',)

    # definindo as colunas liberadas para ediçao na tela de listagem
    list_editable = ()


# definindo as configurações de exibição da Variacao na área administrativa
class VariacaoAdmin(admin.ModelAdmin):

    # definindo as colunas a serem exibidas
    list_display = ('id', 'nome', 'preco',
                    'preco_promocional', 'estoque', 'id_produto')

    # definindo em quais colunas serão colocados links de edição
    list_display_links = ('id', 'nome',)

    # definindo o limite de registros por página
    list_per_page = 10

    # definindo as colunas a serem consideradas no campo de pesquisa
    search_fields = ('nome',)

    # definindo as colunas liberadas para ediçao na tela de listagem
    list_editable = ('preco', 'preco_promocional', 'estoque',)


# registrando as models para exibição na área administrativa
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao, VariacaoAdmin)
