#!/bin/bash

if ! [ -x "$(command -v docker compose)" ]; then
  echo 'Error: docker compose is not installed.' >&2
  exit 1
fi

domains=(yourdomain.ru www.yourdomain.ru)
rsa_key_size=4096
data_path="./data/certbot"
email="youremail@gmail.com"
staging=0

if [ -d "$data_path/conf/live/${domains[0]}" ]; then
  echo "Сертификат уже существует для ${domains[*]}"
  exit 0
fi

echo "### Создание директорий для certbot ..."
mkdir -p "$data_path/conf"
mkdir -p "$data_path/www"

echo "### Запуск nginx ..."
docker compose up -d nginx

echo "### Запрос сертификата для доменов ${domains[*]} ..."
docker compose run --rm --entrypoint "
  certbot certonly --webroot -w /var/www/certbot \
    -d ${domains[0]} -d ${domains[1]} \
    --email $email \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot

echo "### Остановка nginx ..."
docker compose down

echo "### Сертификаты для доменов ${domains[*]} получены и установлены."
