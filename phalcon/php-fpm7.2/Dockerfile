FROM php:7.2-fpm

# fork from phalconphp/php-fpm:7.2-min

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
# libjpeg-dev
# libpng-dev 為了要安裝jpeg
# libfreetype6-dev 可以寫字到圖片上
# libgmp-dev 為了要裝gmp，裝gmp是為了要用套件jose，這個套件是為了要使用sign in with apple
# 修改fpm最大process from 3 => 20
# 2024-03-25 嘗試重新build更新內容

RUN apt update \
&& apt install -y git zip \
&& git clone --depth=1 --branch 3.4.x --single-branch "https://github.com/phalcon/cphalcon.git" \
&& cd cphalcon/build \
&& ./install \
&& cp ../tests/_ci/phalcon.ini $(php-config --configure-options | grep -o "with-config-file-scan-dir=\([^ ]*\)" | awk -F'=' '{print $2}') \
&& cd ../../ \
&& rm -r cphalcon \
&& apt install -y git libxml2-dev libcurl4-gnutls-dev zlib1g-dev libmemcached-dev libpng-dev libjpeg-dev libfreetype6-dev libgmp-dev\
&& pecl install mongodb memcached\
&& docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
&& docker-php-ext-install gd exif mbstring zip mysqli gmp bcmath\
&& docker-php-ext-enable mongodb memcached gd exif mbstring zip mysqli gmp bcmath\
&& curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer\
&& cd /tmp\
&& git clone https://github.com/php/pecl-search_engine-solr.git\
&& cd pecl-search_engine-solr\
&& phpize\
&& ./configure\
&& make\
&& make install\
&& rm -rf /tmp/pecl-search_engine-solr\
&& docker-php-ext-enable solr \
&& apt clean \
&& rm -rf /var/lib/apt/lists/* \
&& pecl clear-cache \ 
&& sed -i 's/pm.max_spare_servers = 3/pm.max_spare_servers = 20/g' /usr/local/etc/php-fpm.d/www.conf \
&& sed -i 's/pm.max_children = 5/pm.max_children = 30/g' /usr/local/etc/php-fpm.d/www.conf

