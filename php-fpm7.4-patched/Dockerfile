# Adapted from docker-library/php 7.4.33 Bullseye FPM.
# Pinned upstream sources and official security patch: PATCH_PROVENANCE.md.

FROM debian:bullseye-slim@sha256:e5b6442dd2e9684cf5e87d8338b5968f3b348636fc0be6d7850a381e3731a2bd

# Bullseye reached end of LTS; retain Debian signature verification.
# Archive metadata is frozen; disable only metadata expiry, never signatures.
RUN printf '%s\n' \
    'deb [check-valid-until=no] http://archive.debian.org/debian bullseye main' \
    'deb [check-valid-until=no] http://archive.debian.org/debian-security bullseye-security main' \
    > /etc/apt/sources.list

# prevent Debian's PHP packages from being installed
# https://github.com/docker-library/php/pull/542
RUN set -eux; \
	{ \
		echo 'Package: php*'; \
		echo 'Pin: release *'; \
		echo 'Pin-Priority: -1'; \
	} > /etc/apt/preferences.d/no-debian-php

# dependencies required for running "phpize"
# (see persistent deps below)
ENV PHPIZE_DEPS \
		autoconf \
		dpkg-dev \
		file \
		g++ \
		gcc \
		libc-dev \
		make \
		pkg-config \
		re2c

# persistent / runtime deps
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		$PHPIZE_DEPS \
		ca-certificates \
		curl \
		xz-utils \
	; \
	rm -rf /var/lib/apt/lists/*

ENV PHP_INI_DIR /usr/local/etc/php
RUN set -eux; \
	mkdir -p "$PHP_INI_DIR/conf.d"; \
# allow running as an arbitrary user (https://github.com/docker-library/php/issues/743)
	[ ! -d /var/www/html ]; \
	mkdir -p /var/www/html; \
	chown www-data:www-data /var/www/html; \
	chmod 777 /var/www/html

# Apply stack smash protection to functions using local buffers and alloca()
# Make PHP's main executable position-independent (improves ASLR security mechanism, and has no performance impact on x86_64)
# Enable optimization (-O2)
# Enable linker optimization (this sorts the hash buckets to improve cache locality, and is non-default)
# https://github.com/docker-library/php/issues/272
# -D_LARGEFILE_SOURCE and -D_FILE_OFFSET_BITS=64 (https://www.php.net/manual/en/intro.filesystem.php)
ENV PHP_CFLAGS="-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
ENV PHP_CPPFLAGS="$PHP_CFLAGS"
ENV PHP_LDFLAGS="-Wl,-O1 -pie"

ENV PHP_VERSION=7.4.33
LABEL org.opencontainers.image.source="https://github.com/php/php-src" \
      org.opencontainers.image.revision="712e60f9edfd03f0960fc4fc3c2c375f42b90aa2" \
      security.php2shell.backport="official-minimal-eol-mitigation"
COPY php-7.4.33.tar.xz security.patch /usr/src/
RUN set -eux; \
    echo '924846abf93bc613815c55dd3f5809377813ac62a9ec4eb3778675b82a27b927  /usr/src/php-7.4.33.tar.xz' | sha256sum -c -; \
    echo '5fe57ca6ee96d59b36c6e0ca842843c50884f177bef1e85234cf669b577f5e48  /usr/src/security.patch' | sha256sum -c -; \
    apt-get update; apt-get install -y --no-install-recommends patch; \
    mkdir -p /usr/src/patched; \
    tar -xJf /usr/src/php-7.4.33.tar.xz -C /usr/src/patched --strip-components=1; \
    cd /usr/src/patched; \
    patch --batch --fuzz=0 -p1 < /usr/src/security.patch; \
    mkdir -p /usr/local/share/php2shell; \
    sha256sum $(sed -n 's!^+++ b/!!p' /usr/src/security.patch) > /usr/local/share/php2shell/source-files.sha256; \
    cp /usr/src/security.patch /usr/local/share/php2shell/; \
    echo 712e60f9edfd03f0960fc4fc3c2c375f42b90aa2 > /usr/local/share/php2shell/commit; \
    tar -cJf /usr/src/php.tar.xz -C /usr/src/patched .; \
    rm -rf /usr/src/patched /usr/src/php-7.4.33.tar.xz /var/lib/apt/lists/*

COPY docker-php-source /usr/local/bin/
COPY pear-channel.xml pecl-channel.xml /usr/local/share/php2shell/channels/

RUN set -eux; \
    echo '7f21f5a755f3d013ca40e79aaa3a94aa7c5ced97cee85a678221c63d804f6322  /usr/local/share/php2shell/channels/pear-channel.xml' | sha256sum -c -; \
    echo '907b20429d188f8b4348b4142e18bd073c8cd811ccc4913a7e2c442d85b5693f  /usr/local/share/php2shell/channels/pecl-channel.xml' | sha256sum -c -; \
	\
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		libargon2-dev \
		libcurl4-openssl-dev \
		libonig-dev \
		libreadline-dev \
		libsodium-dev \
		libsqlite3-dev \
		libssl-dev \
		libxml2-dev \
		zlib1g-dev \
	; \
	\
	export \
		CFLAGS="$PHP_CFLAGS" \
		CPPFLAGS="$PHP_CPPFLAGS" \
		LDFLAGS="$PHP_LDFLAGS" \
	; \
	docker-php-source extract; \
	cd /usr/src/php; \
	gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
	debMultiarch="$(dpkg-architecture --query DEB_BUILD_MULTIARCH)"; \
# https://bugs.php.net/bug.php?id=74125
	if [ ! -d /usr/include/curl ]; then \
		ln -sT "/usr/include/$debMultiarch/curl" /usr/local/include/curl; \
	fi; \
	./configure \
		--build="$gnuArch" \
		--with-config-file-path="$PHP_INI_DIR" \
		--with-config-file-scan-dir="$PHP_INI_DIR/conf.d" \
		\
# make sure invalid --configure-flags are fatal errors instead of just warnings
		--enable-option-checking=fatal \
		\
# https://github.com/docker-library/php/issues/439
		--with-mhash \
		\
# https://github.com/docker-library/php/issues/822
		--with-pic \
		\
# --enable-ftp is included here because ftp_ssl_connect() needs ftp to be compiled statically (see https://github.com/docker-library/php/issues/236)
		--enable-ftp \
# --enable-mbstring is included here because otherwise there's no way to get pecl to use it properly (see https://github.com/docker-library/php/issues/195)
		--enable-mbstring \
# --enable-mysqlnd is included here because it's harder to compile after the fact than extensions are (since it's a plugin for several extensions, not an extension in itself)
		--enable-mysqlnd \
# https://wiki.php.net/rfc/argon2_password_hash
		--with-password-argon2 \
# https://wiki.php.net/rfc/libsodium
		--with-sodium=shared \
# always build against system sqlite3 (https://github.com/php/php-src/commit/6083a387a81dbbd66d6316a3a12a63f06d5f7109)
		--with-pdo-sqlite=/usr \
		--with-sqlite3=/usr \
		\
		--with-curl \
		--with-iconv \
		--with-openssl \
		--with-readline \
		--with-zlib \
		\
# https://github.com/bwoebi/phpdbg-docs/issues/1#issuecomment-163872806 ("phpdbg is primarily a CLI debugger, and is not suitable for debugging an fpm stack.")
		--disable-phpdbg \
		\
# in PHP 7.4+, the pecl/pear installers are officially deprecated (requiring an explicit "--with-pear")
		--with-pear \
		\
# bundled pcre does not support JIT on s390x
# https://manpages.debian.org/bullseye/libpcre3-dev/pcrejit.3.en.html#AVAILABILITY_OF_JIT_SUPPORT
		$(test "$gnuArch" = 's390x-linux-gnu' && echo '--without-pcre-jit') \
		--with-libdir="lib/$debMultiarch" \
		\
		--disable-cgi \
		\
		--enable-fpm \
		--with-fpm-user=www-data \
		--with-fpm-group=www-data \
	; \
	make -j "${BUILD_JOBS:-4}"; \
	find -type f -name '*.a' -delete; \
	make install; \
	find \
		/usr/local \
		-type f \
		-perm '/0111' \
		-exec sh -euxc ' \
			strip --strip-all "$@" || : \
		' -- '{}' + \
	; \
	make clean; \
	\
# https://github.com/docker-library/php/issues/692 (copy default example "php.ini" files somewhere easily discoverable)
	cp -v php.ini-* "$PHP_INI_DIR/"; \
	\
	cd /; \
	docker-php-source delete; \
	\
# reset apt-mark's "manual" list so that "purge --auto-remove" will remove all build dependencies
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
	find /usr/local -type f -executable -exec ldd '{}' ';' \
		| awk '/=>/ { print $(NF-1) }' \
		| sort -u \
		| xargs -r dpkg-query --search \
		| cut -d: -f1 \
		| sort -u \
		| xargs -r apt-mark manual \
	; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	rm -rf /var/lib/apt/lists/*; \
	\
# update from verified local metadata; live PECL returned invalid XML in CI
	pear channel-update /usr/local/share/php2shell/channels/pear-channel.xml; \
	pecl channel-update /usr/local/share/php2shell/channels/pecl-channel.xml; \
	rm -rf /tmp/pear ~/.pearrc; \
	\
# smoke test
	php --version

COPY docker-php-ext-* docker-php-entrypoint /usr/local/bin/

# sodium was built as a shared module (so that it can be replaced later if so desired), so let's enable it too (https://github.com/docker-library/php/issues/598)
RUN docker-php-ext-enable sodium \
    && echo 'session.upload_progress.enabled=Off' > "$PHP_INI_DIR/conf.d/zz-php2shell.ini"

ENTRYPOINT ["docker-php-entrypoint"]
WORKDIR /var/www/html

RUN set -eux; \
	cd /usr/local/etc; \
	if [ -d php-fpm.d ]; then \
		# for some reason, upstream's php-fpm.conf.default has "include=NONE/etc/php-fpm.d/*.conf"
		sed 's!=NONE/!=!g' php-fpm.conf.default | tee php-fpm.conf > /dev/null; \
		cp php-fpm.d/www.conf.default php-fpm.d/www.conf; \
	else \
		# PHP 5.x doesn't use "include=" by default, so we'll create our own simple config that mimics PHP 7+ for consistency
		mkdir php-fpm.d; \
		cp php-fpm.conf.default php-fpm.d/www.conf; \
		{ \
			echo '[global]'; \
			echo 'include=etc/php-fpm.d/*.conf'; \
		} | tee php-fpm.conf; \
	fi; \
	{ \
		echo '[global]'; \
		echo 'error_log = /proc/self/fd/2'; \
		echo; echo '; https://github.com/docker-library/php/pull/725#issuecomment-443540114'; echo 'log_limit = 8192'; \
		echo; \
		echo '[www]'; \
		echo '; if we send this to /proc/self/fd/1, it never appears'; \
		echo 'access.log = /proc/self/fd/2'; \
		echo; \
		echo 'clear_env = no'; \
		echo; \
		echo '; Ensure worker stdout and stderr are sent to the main error log.'; \
		echo 'catch_workers_output = yes'; \
		echo 'decorate_workers_output = no'; \
	} | tee php-fpm.d/docker.conf; \
	{ \
		echo '[global]'; \
		echo 'daemonize = no'; \
		echo; \
		echo '[www]'; \
		echo 'listen = 9000'; \
	} | tee php-fpm.d/zz-docker.conf

# Override stop signal to stop process gracefully
# https://github.com/php/php-src/blob/17baa87faddc2550def3ae7314236826bc1b1398/sapi/fpm/php-fpm.8.in#L163
STOPSIGNAL SIGQUIT

EXPOSE 9000
CMD ["php-fpm"]
