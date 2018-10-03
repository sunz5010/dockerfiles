#https://github.com/phalcon/dockerfiles/blob/master/php-fpm/7.2-min/Dockerfile
FROM phalconphp/php-fpm:7.2-min

# 本dockerfiles增加的項目如下
# git
# php-mongodb
# php-memcached
# php-solr
# php-gd
# php-exif
# php-mbstring
# composer

# 注意，這邊不能用 phpenmod，要用docker-php-ext-enable
# 注意，安裝php extention 用 docker-php-ext-install
# git libxml2 libxml2-dev libcurl4-gnutls-dev 這個是為了要安裝php solr
# zlib1g-dev 這個是為了要安裝memcahced
# libpng-dev 為了要安裝gd

RUN apt update \
&& apt install -y git libxml2-dev libcurl4-gnutls-dev zlib1g-dev libmemcached-dev libpng-dev\
&& pecl install mongodb memcached\
&& docker-php-ext-install gd exif mbstring zip\
&& docker-php-ext-enable mongodb memcached gd exif mbstring zip\
&& curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer\
&& cd /tmp\
&& git clone https://github.com/php/pecl-search_engine-solr.git\
&& cd pecl-search_engine-solr\
&& phpize\
&& ./configure\
&& make\
&& make install\
&& rm -rf /tmp/pecl-search_engine-solr\
&& docker-php-ext-enable solr
