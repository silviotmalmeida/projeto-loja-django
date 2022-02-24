# importação default
from django.contrib import admin
# importando as models do app
from .models import Perfil


# definindo as configurações de exibição do Perfil na área administrativa
class PerfilAdmin(admin.ModelAdmin):

    # definindo as colunas a serem exibidas
    list_display = ('id', 'id_usuario', 'cpf',)

    # definindo em quais colunas serão colocados links de edição
    list_display_links = ('id',)

    # definindo o limite de registros por página
    list_per_page = 10

    # definindo as colunas a serem consideradas no campo de pesquisa
    search_fields = ('id', 'cpf')

    # definindo as colunas liberadas para ediçao na tela de listagem
    list_editable = ()


# registrando as models para exibição na área administrativa
admin.site.register(Perfil, PerfilAdmin)
