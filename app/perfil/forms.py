# importação default
from django import forms

# importando a model User do django
from django.contrib.auth.models import User

# importando as models de perfil
from . import models

# importando a biblioteca de expressões regulares
import re


# formulário responsável pelo cadastro do perfil de um usuário
class PerfilForm(forms.ModelForm):

    # customizando o formulário
    class Meta:
        # definindo a model
        model = models.Perfil
        # definindo os campos a serem exibidos
        fields = '__all__'
        # definindo os campos a serem ocultados
        exclude = ('id_usuario',)


# formulário responsável pelo cadastro de um usuário django
class UserForm(forms.ModelForm):

    # adicionando o campo password ao formulário
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )

    # adicionando o campo password2 ao formulário
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    # customizando o método construtor da classe, adicionando o atributo user
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # atribuindo o user
        self.user = user

    # customizando o formulário
    class Meta:
        # definindo a model
        model = User
        # definindo os campos a serem exibidos
        fields = ('first_name', 'last_name', 'username', 'password',
                  'password2', 'email')

    # definindo as validações do formulário
    def clean(self, *args, **kwargs):

        # obtendo os dados sanitizados do formulário
        data = self.data

        # obtendo os dados sanitizados do formulário
        cleaned = self.cleaned_data

        # inicializando a lista de erros de validação
        validation_error_msgs = {}

        # obtendo os dados do formulário
        username_data = cleaned.get('username')
        email_data = data.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        # consultando se o username já é utilizado
        username_db = User.objects.filter(username=username_data).first()

        # consultando se o email já é utilizado
        email_db = User.objects.filter(email=email_data).first()

        # definindo os textos dos erros de validação
        error_msg_username_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_email_invalid = 'Informe um endereço de email válido'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        # se o atributo de classe user estiver definido, trata-se de uma atualização
        if self.user:
            # se o username já estiver sendo utilizado
            if username_db:
                # se o username do formulário for diferente do cadastrado no bd
                if username_data != username_db.username:
                    # adiciona um erro de validação
                    validation_error_msgs['username'] = error_msg_username_exists

            # se o email já estiver sendo utilizado
            if email_db:
                # se o email do formulário for diferente do cadastrado no bd
                if email_data != email_db.email:
                    # adiciona um erro de validação
                    validation_error_msgs['email'] = error_msg_email_exists

            # se password foi preenchido
            if password_data:
                # se o password for diferente do password2
                if password_data != password2_data:
                    # adiciona um erro de validação
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                # se o tamanho do password for menor que 6
                if len(password_data) < 6:
                    # adiciona um erro de validação
                    validation_error_msgs['password'] = error_msg_password_short

        # se o atributo de classe user não estiver definido, trata-se de um novo cadastro
        else:
            # se o username já estiver sendo utilizado
            if username_db:
                # adiciona um erro de validação
                validation_error_msgs['username'] = error_msg_username_exists

            # se o email já estiver sendo utilizado
            if email_db:
                # adiciona um erro de validação
                validation_error_msgs['email'] = error_msg_email_exists

            if len(email_data) < 1:
                # adiciona um erro de validação
                validation_error_msgs['email'] = error_msg_email_invalid

            # se password não foi preenchido
            if not password_data:
                # adiciona um erro de validação
                validation_error_msgs['password'] = error_msg_required_field

            # se password2 não foi preenchido
            if not password2_data:
                # adiciona um erro de validação
                validation_error_msgs['password2'] = error_msg_required_field

            # se o password for diferente do password2
            if password_data != password2_data:
                # adiciona um erro de validação
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

            # se o tamanho do password for menor que 6
            if len(password_data) < 6:
                # adiciona um erro de validação
                validation_error_msgs['password'] = error_msg_password_short

        # se existirem erros de validação
        if validation_error_msgs:
            # levanta uma exceção com os referidos erros
            raise(forms.ValidationError(validation_error_msgs))
