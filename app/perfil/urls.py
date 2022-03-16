# importação default
from django.urls import path

# importando as views do app
from . import views


# definindo o nome do perfil como namespace
app_name = 'perfil'

# definindo os endpoints do app
urlpatterns = [
    # definindo o endpoint de criação e atualização de perfis
    path('', views.Create.as_view(), name='create'),
    # definindo o endpoint de login
    path('login/', views.Login.as_view(), name='login'),
    # definindo o endpoint de logout
    path('logout/', views.Logout.as_view(), name='logout'),
]
