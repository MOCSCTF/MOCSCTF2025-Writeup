FROM php:7.3-fpm-alpine3.15

# 安装必要的软件包
# 增加 curl 用于下载 Composer，以及 git (Composer 可能需要 git 来下载某些依赖)
RUN apk update && apk add --no-cache nginx bash curl git

# 安装 Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && rm -rf /var/cache/apk/* # 清理 apk 缓存

# 拷贝容器入口点脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 复制nginx配置文件
COPY ./config/nginx.conf /etc/nginx/nginx.conf

# 复制web项目源码
COPY src /var/www/html

# 重新设置源码路径的用户所有权

RUN chown -R www-data:www-data /var/www/html

# 设置shell的工作目录
WORKDIR /var/www/html

# 在这里添加 Guzzle 的安装步骤
# 切换到 www-data 用户，以便 Composer 可以写入文件（如 composer.json, vendor 目录）
USER www-data
# 如果你的项目 src 目录下已经有 composer.json，建议使用 `composer install --no-dev`
# 如果你只是想添加 Guzzle 并且让 Composer 自动创建或更新 composer.json，使用 `composer require`
RUN composer require guzzlehttp/guzzle 

# 切换回 root 用户，如果后续操作需要 root 权限
USER root

# 设置nginx日志保存目录
VOLUME ["/var/log/nginx"]

COPY flag.txt /flag.txt

# 设置容器入口点
ENTRYPOINT [ "/docker-entrypoint.sh" ]
EXPOSE 80