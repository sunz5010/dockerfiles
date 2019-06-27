FROM alpine/git
WORKDIR /tmp
RUN git clone --branch phalcon-v2.0.13 --depth 1 https://github.com/phalcon/cphalcon.git cphalcon

FROM php:5.6-fpm
WORKDIR /tmp
COPY --from=0 /tmp/cphalcon /tmp/cphalcon
RUN apt update \
&& apt install -y libpcre3-dev libssl-dev libcurl4-openssl-dev zlib1g-dev libmcrypt-dev \
&& apt install -y libmemcached-dev libpng-dev libmagickwand-dev libxml2-dev libcurl4-gnutls-dev \
&& cd cphalcon/build \
&& ./install \
&& printf "\n" | pecl install mongo \
&& pecl install mongodb \
&& printf "\n" | pecl install memcache \
&& printf "\n" | pecl install memcached-2.2.0 \
&& printf "\n" | pecl install imagick \
&& printf "\n\n\n" | pecl install solr \
&& docker-php-ext-install gd exif zip mcrypt \
&& docker-php-ext-enable phalcon mongo mongodb memcache memcached imagick solr mcrypt\
&& cd /tmp \
&& rm -Rf cphalcon \
&& apt clean \
&& rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/html/
