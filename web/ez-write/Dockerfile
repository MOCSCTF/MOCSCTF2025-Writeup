FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# USER 1000

RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    php-mysql \
    php-cli \
    php-curl \
    php-gd \
    php-mbstring \
    php-xml \
    php-zip \
    php-iconv \
    wget \
    unzip \
    libzip-dev \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    locales \
    vim-common \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN locale-gen zh_CN.UTF-8
ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN:zh
ENV LC_ALL=zh_CN.UTF-8

RUN rm -f /var/www/html/index.html

COPY src/index.php /var/www/html
COPY flag.txt /flag.txt
RUN chmod 400 /flag.txt
RUN mkdir -p /var/www/html/tmp
RUN chown -R www-data:www-data /var/www/html/tmp

RUN chmod u+s /usr/bin/xxd

RUN a2enmod rewrite

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
