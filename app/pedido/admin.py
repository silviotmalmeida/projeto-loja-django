# importação default
from django.contrib import admin
# importando as models do app
from .models import Pedido, ItemPedido


# definindo as configurações de exibição do ItemPedido na área administrativa da model Pedido
class ItemPedidoInline(admin.TabularInline):
    # model a ser utilizado
    model = ItemPedido
    # quantidade de variações em branco a serem exibidas
    extra = 0


# definindo as configurações de exibição do Pedido na área administrativa
class PedidoAdmin(admin.ModelAdmin):

    # definindo as demais models a serem apresentadas
    inlines = [ItemPedidoInline]

    # definindo as colunas a serem exibidas
    list_display = ('id', 'total', 'status', 'id_usuario',)

    # definindo em quais colunas serão colocados links de edição
    list_display_links = ('id',)

    # definindo o limite de registros por página
    list_per_page = 10

    # definindo as colunas a serem consideradas no campo de pesquisa
    search_fields = ('id',)

    # definindo as colunas liberadas para ediçao na tela de listagem
    list_editable = ()


# definindo as configurações de exibição do ItemPedido na área administrativa
class ItemPedidoAdmin(admin.ModelAdmin):

    # definindo as colunas a serem exibidas
    list_display = ('id', 'id_pedido', 'nome_produto',
                    'nome_variacao', 'preco', 'quantidade',)

    # definindo em quais colunas serão colocados links de edição
    list_display_links = ('id',)

    # definindo o limite de registros por página
    list_per_page = 10

    # definindo as colunas a serem consideradas no campo de pesquisa
    search_fields = ('id', 'nome_produto', 'nome_variacao',)

    # definindo as colunas liberadas para ediçao na tela de listagem
    list_editable = ()


# registrando as models para exibição na área administrativa
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)
