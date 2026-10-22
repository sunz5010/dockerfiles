# Published, accepted PHP 7.4.33 mitigation base; currently linux/arm64 only.
FROM luofofo/php-fpm7.4-patched:7.4.33-php2shell-20261022-712e60f9edfd-arm64@sha256:df302e995c224f019b64ac33324fd74ae1a7acd4724d6881effd33c5ccf410d0

# phalcon 4.x

# 本dockerfiles增加的項目如下
# git
# php-mongodb
# php-memcached
# php-solr
# php-gd
# php-exif
# php-mbstring
# php-zip 給composer安裝的時候，不要去clone git repo，導致vendor裡面有.git資料夾
# mysqli 這邊是為了給wordpress用的
# composer

# 注意，這邊不能用 phpenmod，要用docker-php-ext-enable
# 注意，安裝php extention 用 docker-php-ext-install
# git libxml2 libxml2-dev libcurl4-gnutls-dev 這個是為了要安裝php solr
# zlib1g-dev 這個是為了要安裝memcahced
# libpng-dev 為了要安裝gd
# libjpeg-dev support h
# libpng-dev 為了要安裝jpeg
# libfreetype6-dev 可以寫字到圖片上
# libgmp-dev 為了要裝gmp，裝gmp是為了要用套件jose，這個套件是為了要使用sign in with apple

# 2020-06-30
# 注意，--with-freetype-dir --with-jpeg-dir 這兩個參數在php7.4改名稱了，改為 --with-freetype --with-jpeg，所以這個設定檔不能支援php7.2
# ref: https://github.com/docker-library/php/issues/931
#
# 多安裝，libonig-dev，新版mbstring需要
# ref: https://github.com/docker-library/php/issues/880
#
# 多安裝，libzip-dev，新版zip需要

COPY SHA256SUMS *.tgz *.tar.gz composer.phar /tmp/extension-sources/
RUN test "$(dpkg --print-architecture)" = arm64 \
 && cd /tmp/extension-sources && sha256sum -c SHA256SUMS

RUN apt-get update \
&& apt-get install -y --no-install-recommends git zip \
&& mkdir php-psr && tar xzf /tmp/extension-sources/psr.tar.gz -C php-psr --strip-components=1 \
&& cd php-psr \
&& phpize \
&& ./configure \
&& make \
&& make install \
&& cd .. \
&& rm -r php-psr \
&& docker-php-ext-enable psr \
&& mkdir cphalcon && tar xzf /tmp/extension-sources/phalcon.tar.gz -C cphalcon --strip-components=1 \
&& cd cphalcon/build \
&& ./install --arch 64bits \
&& cp ../.ci/phalcon.ini "$PHP_INI_DIR/conf.d/phalcon.ini" \
&& cd ../../ \
&& rm -r cphalcon \
&& apt-get install -y --no-install-recommends git libxml2-dev libcurl4-gnutls-dev zlib1g-dev libmemcached-dev libpng-dev libjpeg-dev libfreetype6-dev libonig-dev libzip-dev libgmp-dev\
&& pecl install /tmp/extension-sources/mongodb-1.20.1.tgz /tmp/extension-sources/memcached-3.2.0.tgz\
&& docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
&& docker-php-ext-install gd exif mbstring zip mysqli gmp bcmath\
&& docker-php-ext-enable mongodb memcached\
&& install -m 0755 /tmp/extension-sources/composer.phar /usr/local/bin/composer\
&& cd /tmp\
&& mkdir pecl-search_engine-solr && tar xzf /tmp/extension-sources/solr.tar.gz -C pecl-search_engine-solr --strip-components=1\
&& cd pecl-search_engine-solr\
&& phpize\
&& ./configure\
&& make\
&& make install\
&& cd /tmp\
&& rm -rf /tmp/pecl-search_engine-solr\
&& docker-php-ext-enable solr \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* \
&& mkdir -p /tmp/pear/cache \
&& pecl clear-cache \
&& rm -rf /tmp/extension-sources
