# Published, accepted PHP 7.4.33 mitigation base for linux/amd64.
FROM luofofo/php-fpm7.4-patched@sha256:d466e418826fb80950063e248863954908ea99f42952b24708e08b949788acb7

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
RUN test "$(dpkg --print-architecture)" = amd64 \
 && cd /tmp/extension-sources && sha256sum -c SHA256SUMS

ARG BUILD_JOBS=4
RUN export MAKEFLAGS="-j${BUILD_JOBS}"; apt-get update \
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

RUN php -r 'if (PHP_VERSION !== "7.4.33" || Phalcon\Version::get() !== "4.1.1") exit(1);' \
 && mkdir -p /usr/local/share/phalcon4-php74
COPY sources.lock.json SHA256SUMS PHALCON_LICENSE.txt THIRD_PARTY_NOTICES.md /usr/local/share/phalcon4-php74/
LABEL org.opencontainers.image.title="PHP 7.4.33 patched FPM with Phalcon 4.1.1 (AMD64)" \
      org.opencontainers.image.version="4.1.1-php7.4.33-php2shell-20261026-amd64" \
      local.phalcon.source="dcb2be7acac3856ecba9b1032ddee9270503a614" \
      local.phalcon.license="BSD-3-Clause"
