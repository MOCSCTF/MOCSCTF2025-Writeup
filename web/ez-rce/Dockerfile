FROM ubuntu:20.04

# 非交互模式安装
ENV DEBIAN_FRONTEND=noninteractive

# 安装 PHP 和 Nginx
RUN apt-get update && apt-get install -y \
    php-fpm \
    php-cli \
    php-mysql \
    nginx \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 拷贝配置和源码
COPY nginx/default.conf /etc/nginx/sites-available/default
COPY src/ /var/www/html/

# 设置工作目录
WORKDIR /var/www/html

# 开放端口
EXPOSE 80

# 启动脚本
CMD service php7.4-fpm start && nginx -g "daemon off;"
