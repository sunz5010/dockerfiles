# Published, accepted PHP 7.4.33 mitigation base; currently linux/amd64 only.
ARG PHP_BASE_IMAGE=luofofo/php-fpm7.4-patched@sha256:d466e418826fb80950063e248863954908ea99f42952b24708e08b949788acb7
FROM ${PHP_BASE_IMAGE}

# Phalcon 3.4.5, with three PHP 7.4 native API compatibility backports.

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

COPY SHA256SUMS *.tgz *.tar.gz composer.phar php74-compat.patch /tmp/extension-sources/
RUN test "$(dpkg --print-architecture)" = amd64 \
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
&& cd cphalcon \
&& patch --batch --fuzz=0 -p1 < /tmp/extension-sources/php74-compat.patch \
&& cd build/php7/64bits \
&& phpize && ./configure --enable-phalcon && make -j4 && make install \
&& echo "extension=phalcon.so" > "$PHP_INI_DIR/conf.d/phalcon.ini" \
&& cd ../../../.. \
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

RUN php -r 'if (PHP_VERSION !== "7.4.33" || Phalcon\Version::get() !== "3.4.5") exit(1);' \
 && mkdir -p /usr/local/share/phalcon3-php74
COPY sources.lock.json php74-compat.patch SHA256SUMS /usr/local/share/phalcon3-php74/
LABEL org.opencontainers.image.title="PHP 7.4.33 patched FPM with Phalcon 3.4.5" \
      org.opencontainers.image.description="PHP2Shell EOL mitigation base; Phalcon 3 API with PHP 7.4 compatibility backports" \
      org.opencontainers.image.version="3.4.5-php7.4.33-php2shell-20261026-r1" \
      org.opencontainers.image.source="https://github.com/sunz5010/dockerfiles/tree/master/phalcon" \
      local.phalcon.license="BSD-3-Clause" \
      local.phalcon.source="d4e0362207fd2f7bdd26feca0b4271056d52a06a" \
      local.phalcon.php74-patch.sha256="a6af3a8cea677405e4ddee12bf538b650915a7f0e439ce69cc5d26ca2d9343eb"
COPY PHALCON_LICENSE.txt THIRD_PARTY_NOTICES.md /usr/local/share/phalcon3-php74/
