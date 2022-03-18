# importação default
from unittest.loader import VALID_MODULE_NAME
from django.db import models
# importando a model de usuário da área administrativa do django
from django.contrib.auth.models import User
# importando dependência para levantar exceções de validação
from django.forms import ValidationError
# importando as bibliotecas de validação de CPF e CEP
from utils.valida_cpf import valida_cpf
from utils.valida_cep import valida_cep


# criando a model de Perfil
class Perfil(models.Model):

    # criando o atributo id_usuario com referência à model Produto, com deleção em cascata
    id_usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')

    # criando o atributo data_nascimento como data
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')

    # criando o atributo cpf como texto com tamanho máximo de 11
    cpf = models.CharField(max_length=11, verbose_name='CPF(somente números)')

    # criando o atributo logradouro como texto com tamanho máximo de 50
    logradouro = models.CharField(max_length=50, verbose_name='Logradouro')

    # criando o atributo numero como texto com tamanho máximo de 5
    numero = models.CharField(max_length=5, verbose_name='Número')

    # criando o atributo complemento como texto com tamanho máximo de 30
    complemento = models.CharField(max_length=30, verbose_name='Complemento')

    # criando o atributo bairro como texto com tamanho máximo de 30
    bairro = models.CharField(max_length=30, verbose_name='Bairro')

    # criando o atributo cep como texto com tamanho máximo de 8
    cep = models.CharField(max_length=8, verbose_name='CEP(somente números)')

    # criando o atributo cidade como texto com tamanho máximo de 30
    cidade = models.CharField(max_length=30, verbose_name='Cidade')

    # criando o atributo estado com opções pré-definidas
    estado = models.CharField(default='SP',
                              max_length=2,
                              choices=(
                                  ('AC', 'Acre'),
                                  ('AL', 'Alagoas'),
                                  ('AP', 'Amapá'),
                                  ('AM', 'Amazonas'),
                                  ('BA', 'Bahia'),
                                  ('CE', 'Ceará'),
                                  ('DF', 'Distrito Federal'),
                                  ('ES', 'Espírito Santo'),
                                  ('GO', 'Goiás'),
                                  ('MA', 'Maranhão'),
                                  ('MT', 'Mato Grosso'),
                                  ('MS', 'Mato Grosso do Sul'),
                                  ('MG', 'Minas Gerais'),
                                  ('PA', 'Pará'),
                                  ('PB', 'Paraíba'),
                                  ('PR', 'Paraná'),
                                  ('PE', 'Pernambuco'),
                                  ('PI', 'Piauí'),
                                  ('RJ', 'Rio de Janeiro'),
                                  ('RN', 'Rio Grande do Norte'),
                                  ('RS', 'Rio Grande do Sul'),
                                  ('RO', 'Rondônia'),
                                  ('RR', 'Roraima'),
                                  ('SC', 'Santa Catarina'),
                                  ('SP', 'São Paulo'),
                                  ('SE', 'Sergipe'),
                                  ('TO', 'Tocantins'),
                              ),
                              verbose_name='Estado')

    # definindo qual atributo da model será exibido na área administrativa
    def __str__(self):
        return f'{self.id_usuario.first_name} {self.id_usuario.last_name}'

    # definindo as validações adicionais a serem realizadas
    def clean(self):

        # inicializando o dicionário de erros
        error_messages = {}

        # se o CEP for inválido, popula o dicionário de erros
        if not valida_cep(self.cep):
            error_messages['cep'] = 'Digite um CEP válido (somente números)'

        # se o CPF for inválido, popula o dicionário de erros
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido (somente números)'

        # se existirem erros, levanta a exceção
        if error_messages:
            raise ValidationError(error_messages)

    # definindo os nomes da model a serem exibidos na área administrativa
    class Meta:
        # nome no singular
        verbose_name = 'Perfil'
        # nome no plural
        verbose_name_plural = 'Perfis'
