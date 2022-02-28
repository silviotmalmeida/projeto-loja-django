# importação default
from django.shortcuts import render

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View


# definindo a view Create
class Create(ListView):
    pass


# definindo a view Update
class Update(ListView):
    pass


# definindo a view Login
class Login(ListView):
    pass


# definindo a view Logout
class Logout(ListView):
    pass
