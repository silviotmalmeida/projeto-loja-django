# importação default
from django.shortcuts import render, get_object_or_404

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View

# importando a model User do django
from django.contrib.auth.models import User

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

        # inicializando o perfil
        self.perfil = None

        # se o usuário estiver autenticado
        if self.request.user.is_authenticated:

            # obtendo o perfil do usuário logado
            self.perfil = models.Perfil.objects.filter(
                id_usuario=self.request.user).first()

            # definindo o contexto a ser passado ao template
            self.context = {
                # passando o formulário de usuário, com dados do POST ou vazio
                # e os dados do usuário logado
                'userform': forms.UserForm(data=self.request.POST or None,
                                           user=self.request.user,
                                           instance=self.request.user),

                # passando o formulário de perfil, com dados do POST ou vazio
                # e os dados do usuário logado
                'perfilform': forms.PerfilForm(data=self.request.POST or None,
                                               perfil=self.perfil,
                                               instance=self.perfil),
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

        # definindo uma variável para o userform
        self.userform = self.context['userform']

        # definindo uma variável para o perfilform
        self.perfilform = self.context['perfilform']

    # definindo a resposta a uma requisição get
    def get(self, *args, **kwargs):

        # renderizando o template
        return self.render_template


# definindo a view Create
# vai herdar de BaseCustomView
class Create(BaseCustomView):

    # definindo a resposta a uma requisição post
    def post(self, *args, **kwargs):

        # se houve alguma falha de validação dos formulários
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            # renderizando o template
            return self.render_template

        # obtendo os dados do formulário
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # se o usuário estiver autenticado, trata-se de uma atualização
        if self.request.user.is_authenticated:

            # criando o objeto do usuário logado
            user = get_object_or_404(User, username=self.request.user.username)

            # atualizando os dados a partir do formulário
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            # se o password for preenchido, altera-o
            if password:
                user.set_password(password)

            # salvando o user no bd
            user.save()

            # criando o objeto perfil com os dados do formulário, sem salvá-lo no bd
            perfil = self.perfilform.save(commit=False)
            # inserindo o id_usuario
            perfil.id_usuario = user
            # salvando o perfil do user no bd
            perfil.save()

        # senão, trata-se de um novo cadastro
        else:

            # criando o objeto user com os dados do formulário, sem salvá-lo no bd
            user = self.userform.save(commit=False)
            # inserindo a senha com criptografia
            user.set_password(password)
            # salvando o user no bd
            user.save()

            # criando o objeto perfil com os dados do formulário, sem salvá-lo no bd
            perfil = self.perfilform.save(commit=False)
            # inserindo o id_usuario
            perfil.id_usuario = user
            # salvando o perfil do user no bd
            perfil.save()

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
