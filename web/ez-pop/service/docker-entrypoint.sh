#!/bin/sh

rm -f /docker-entrypoint.sh

chmod 744 /flag.txt

php-fpm & nginx &

echo "Running..."

tail -F /var/log/nginx/access.log /var/log/nginx/error.log