#!/bin/bash

echo "Definindo permissoes da pasta de código-fonte..."
docker container exec loja-django chmod 777 -R /root
sleep 1

echo "Iniciando o servidor..."
docker container exec -it loja-django python3 /root/manage.py runserver 0.0.0.0:8080

