# Projeto LOJA-DJANGO

## Projeto Final construído durante o curso "Curso de Python 3 do Básico Ao Avançado (com projetos reais)" do professor Luiz Otávio Miranda.

Trata-se da implementação de uma loja virtual.

O projeto encontra-se dockerizado para facilitar a implantação. As orientações para execução estão listadas abaixo:

- Criar e carregar a imagem docker loja-django conforme passos da pasta image;

- Para iniciar o container utiliza-se o comando "sudo ./startContainers.sh";

- Para criar o BD utiliza-se o comando "sudo ./runMigrate.sh";

- Para criar o Administrador do Sistema utiliza-se o comando "sudo ./runCreateSuperUser.sh";

- Para iniciar o servidor utiliza-se o comando "sudo ./runServer.sh";

- O sistema estará disponível na URL "0.0.0.0:8080";

- Para carregar os dados de teste utiliza-se a URL "0.0.0.0:8080/loadtestdata/"

- Para encerrar a execução utiliza-se o comando "sudo ./stopContainers.sh";

Foram incluídos diversos comentários para facilitar o entendimento do código.


Principais comandos do django:

- Para criar um projeto django utiliza o comando: django-admin startproject nome-do-projeto .

- Para criar um app utiliza o comando dentro da pasta do projeto: python3 manage.py startapp nome-do-app

- Para criar as migrations utiliza o comando dentro da pasta do projeto: python3 manage.py makemigrations

- Para aplicar as migrations utiliza o comando dentro da pasta do projeto: python3 manage.py migrate

- Para criar o superusuário da área administrativa utiliza o comando dentro da pasta do projeto: python3 manage.py createsuperuser

- Para iniciar o servidor de desenvolvimento utiliza o comando dentro da pasta do projeto: python3 manage.py runserver 0.0.0.0:8080
