# importação default
from django.shortcuts import render, get_object_or_404, redirect

# importando os tipos de views a serem utilizadas
from django.views.generic.list import ListView
from django.views import View

# importando a model User do django
from django.contrib.auth.models import User

# importando as funções de autenticação do django
from django.contrib.auth import authenticate, login

# importando as models do app
from . import models

# importando os forms do app
from . import forms

# biblioteca para cópia de objetos
import copy

# importando as mensagens do django
from django.contrib import messages



# definindo a view BaseCustomView
class BaseCustomView(View):

    # definindo o template a ser utilizado
    template_name = 'perfil/create.html'

    # customizando a view
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        # criando uma cópia do carrinho da sessão
        self.cart = copy.deepcopy(self.request.session.get('cart'), {})

        # inicializando o perfil
        self.perfil = None

        # se o usuário estiver autenticado
        if self.request.user.is_authenticated:

            # altera o template a ser utilizado
            self.template_name = 'perfil/update.html'

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
# possui a função de criar e editar usuários e perfis
class Create(BaseCustomView):

    # definindo a resposta a uma requisição post
    def post(self, *args, **kwargs):

        # se houve alguma falha de validação dos formulários
        if not self.userform.is_valid() or not self.perfilform.is_valid():

            # envia mensagem de erro
            messages.error(self.request, 'Foram encontrados erros no formulário.')

            # renderizando o template mantendo os dados no POST
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

        # se o password foi preenchido
        if password:

            # verifica a validade dos dados de autenticação
            is_user = authenticate(
                self.request, username=self.request.user.username, password=password)

            # realiza o login
            if is_user:
                login(self.request, user=user)

        # recriando o carrinho da sessão para evitar a perda do carrinho na edição do usuário
        self.request.session['cart'] = self.cart

        # salvando a sessão
        self.request.session.save()

        # enviando mensagem de sucesso  
        messages.success(self.request, 'Operação realizada com sucesso!')

        # reabre o template sem os dados no POST
        return redirect('perfil:create')


# definindo a view Login
class Login(ListView):
    pass


# definindo a view Logout
class Logout(ListView):
    pass
