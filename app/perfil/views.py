# importação default
from django.shortcuts import render

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View

# importando as models do app
from . import models

# importando os forms do app
from . import forms


# definindo a view BaseCustomView
class BaseCustomView(View):

    # definindo o template a ser utilizado
    template_name = 'perfil/create.html'

    # customizando a view
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        # se o usuário estiver autenticado
        if self.request.user.is_authenticated:

            # definindo o contexto a ser passado ao template
            self.context = {
                # passando o formulário de usuário, com dados do POST ou vazio
                # e os dados do usuário logado
                'userform': forms.UserForm(data=self.request.POST or None,
                                           user=self.request.user,
                                           instance=self.request.user),

                # passando o formulário de perfil, com dados do POST ou vazio
                # e os dados do usuário logado
                'perfilform': forms.PerfilForm(data=self.request.POST or None),
            }
        else:
            # definindo o contexto a ser passado ao template
            self.context = {
                # passando o formulário de usuário, com dados do POST ou vazio
                'userform': forms.UserForm(data=self.request.POST or None),

                # passando o formulário de perfil, com dados do POST ou vazio
                'perfilform': forms.PerfilForm(data=self.request.POST or None),
            }

        # definindo o método de renderização
        self.render_template = render(
            self.request, self.template_name, self.context)

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # renderizando o template
        return self.render_template


# definindo a view Create
# vai herdar de BaseCustomView
class Create(BaseCustomView):

    # definindo a resposta a uma requisição post
    def post(self, *args, **kwargs):

        # renderizando o template
        return self.render_template


# definindo a view Update
class Update(ListView):
    pass


# definindo a view Login
class Login(ListView):
    pass


# definindo a view Logout
class Logout(ListView):
    pass
