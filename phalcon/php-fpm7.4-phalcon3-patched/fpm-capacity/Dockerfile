# Preserve the published Phalcon 3.4.5 / PHP 7.4.33 / Brotli 1.0.10 runtime.
FROM luofofo/phalcon-php-fpm7.4-patched@sha256:58f811169eb23a1f936e901671ae29f3f75d2b0496fa28584e9d267ae075f6ef

# Restore the original PHP 7.2 pool capacity without changing other settings.
RUN sed -i 's/pm.max_spare_servers = 3/pm.max_spare_servers = 20/g' /usr/local/etc/php-fpm.d/www.conf \
 && sed -i 's/pm.max_children = 5/pm.max_children = 30/g' /usr/local/etc/php-fpm.d/www.conf \
 && grep -qx 'pm.max_spare_servers = 20' /usr/local/etc/php-fpm.d/www.conf \
 && grep -qx 'pm.max_children = 30' /usr/local/etc/php-fpm.d/www.conf \
 && php-fpm -t
