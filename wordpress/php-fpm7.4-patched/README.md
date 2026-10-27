# WordPress / patched PHP 7.4 FPM — AMD64

PHP-FPM runtime for an existing WordPress installation, based on the accepted
Phalcon 4.1.1 / PHP 7.4.33 patched image with MongoDB extension 1.19.4.
This recipe builds Linux AMD64 (`x86_64`).

## Published image

```sh
docker pull luofofo/wordpress-phalcon-php-fpm7.4:4.1.1-php7.4.33-php2shell-20261027-mongo1.19.4-amd64
```

Pin the accepted release:

```dockerfile
FROM luofofo/wordpress-phalcon-php-fpm7.4@sha256:cdbc0ff08710f331c382e91b82ad0b1fea29e1839f759df21474b87c1acf173c
```

The existing Docker Hub `latest` tag remains unchanged. Use the explicit tag
above for the patched runtime.

## Build

Run from the repository root:

```sh
docker build --platform=linux/amd64 -t wordpress-php74-patched:local wordpress/php-fpm7.4-patched
```

The [Dockerfile](Dockerfile) retains the original WordPress package install
steps, Imagick 3.4.4 pin, OPcache settings and error logging settings.
Its base is the [Phalcon 4 patched recipe](../../phalcon/php-fpm7.4-patched/).

| Component | Runtime version |
| --- | --- |
| PHP | 7.4.33 |
| Phalcon | 4.1.1 |
| MongoDB extension | 1.19.4 |
| Memcached extension | 3.2.0 |
| Solr extension | 2.8.1 |
| Imagick extension | 3.4.4 |
| Ghostscript | 9.53.3 |

GD with JPEG/FreeType, EXIF, MySQLi, ZIP, BCMath and OPcache are retained.
These runtime versions include the selected base's packages; preserving
installation steps does not freeze the older base image's versions.

The image keeps the PHP-FPM entrypoint, `/var/www/html`, port 9000, www-data
UID/GID 33 and SIGQUIT. Supply your existing WordPress files and configuration,
and a FastCGI server such as Nginx. This image does not install or upgrade
WordPress core or plugins.

See [VALIDATION.md](VALIDATION.md) for the accepted artifact and test scope.
