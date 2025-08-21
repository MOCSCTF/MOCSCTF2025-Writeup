FROM php:7.0.9-apache

WORKDIR /var/www/html

COPY src/execute.php /var/www/html
COPY src/index.php /var/www/html
COPY src/init.sh /init.sh
COPY flag.txt /flag.txt

RUN chmod +x /init.sh

RUN rm -f /var/www/html/index.html

RUN a2enmod rewrite

CMD ["/init.sh"]

EXPOSE 80
