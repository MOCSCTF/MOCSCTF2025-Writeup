FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    nginx \
    php-fpm \
    php-mysqli \
    && rm -rf /var/lib/apt/lists/*

COPY nginx/default.conf /etc/nginx/sites-available/default

COPY src/ /var/www/html/
COPY flag.txt /flag.txt
EXPOSE 9999

CMD service nginx start && service php7.0-fpm start && tail -f /dev/null