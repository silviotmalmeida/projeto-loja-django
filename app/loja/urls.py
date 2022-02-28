"""loja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# foi importado também o include, para permitir a inclusão das urls do app
from django.urls import path, include
# importações para carregamento de imagens no sistema
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('produto.urls')),
    path('perfil/', include('perfil.urls')),
    path('pedido/', include('pedido.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # adicionando variáveis para suportar o carregamento de imagens


# FIXME: manter somente em ambiente de desenvolvimento
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [

        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
