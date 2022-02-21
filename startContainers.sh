#!/bin/bash

echo "Subindo o container..."
docker-compose up -d --remove-orphans

sleep 5

echo "Definindo permissoes da pasta de código-fonte..."
docker container exec loja-django chmod 777 -R /root
sleep 1

echo "Processo concluído."
