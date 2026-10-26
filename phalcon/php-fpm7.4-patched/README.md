# Phalcon 4.1.1 / patched PHP 7.4.33 FPM — AMD64

This recipe builds **linux/amd64** (Linux `x86_64`) using the accepted patched
PHP 7.4.33 base. The earlier ARM64 Phalcon 4 recipe is replaced by this AMD64
recipe; the old ARM64 Docker Hub tag is retired.

Phalcon 4 has different application APIs from Phalcon 3. Existing Phalcon 3
applications should use the separate
[Phalcon 3.4.5 compatibility recipe](../php-fpm7.4-phalcon3-patched/).

## Published image

Docker Hub: [luofofo/phalcon-php-fpm7.4-patched](https://hub.docker.com/r/luofofo/phalcon-php-fpm7.4-patched/tags?name=4.1.1).

```sh
docker pull luofofo/phalcon-php-fpm7.4-patched:4.1.1-php7.4.33-php2shell-20261027-mongo1.19.4-amd64
```

The validation result is recorded in [VALIDATION.md](VALIDATION.md). This recipe does not overwrite `latest` or any
Phalcon 3 tags.


MongoDB 1.19.4 is intentionally pinned for older libraries that pass integer
`ReadPreference::RP_*` modes. CLI and FPM acceptance promote PHP warnings to
exceptions while checking these legacy modes. Existing 2026-10-26 tags are kept
for rollback; no existing tag is overwritten. This is a compatibility pin, not
a claim that older MongoDB libraries or extensions receive current security fixes.

## Build and test

Requirements: Docker/buildx, Python 3, and network access for SHA256-verified
source downloads and Debian archive packages. Run from this directory:

```sh
./build.sh
./test.sh
```

Default local image:
`phalcon74-patched:4.1.1-php7.4.33-php2shell-20261027-mongo1.19.4-amd64`.
Set `PHALCON74_IMAGE` to use another local tag. On an ARM64 host, configure
AMD64 execution support (such as QEMU) before building or testing.
Build and acceptance evidence is written to ignored `reports/`.

For a direct Docker build, first prepare and validate all inputs:

```sh
python3 fetch-inputs.py
docker build --platform=linux/amd64 -t phalcon74-patched:local .
PHALCON74_IMAGE=phalcon74-patched:local ./test.sh
```

`python3 fetch-inputs.py --offline` validates an already prepared context.
Sources are locked in `sources.lock.json` and `SHA256SUMS` and are excluded
from Git. Existing inputs with invalid hashes are rejected, not overwritten.
The Dockerfile verifies them again. `BUILD_JOBS` defaults to 4 for compilation;
no host-specific instruction-set requirements are deliberately enabled.

## Base and extensions

```dockerfile
FROM luofofo/php-fpm7.4-patched@sha256:d466e418826fb80950063e248863954908ea99f42952b24708e08b949788acb7
```

The base contains official PHP EOL mitigation commit
`712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`. PHP CLI/FPM/phpize/php-config
hashes must equal this accepted base, and all 17 official patched source-file
hashes are checked independently.

Phalcon 4.1.1 is built from official commit
`dcb2be7acac3856ecba9b1032ddee9270503a614`, using its 64-bit source and API.
PSR 1.2.0, MongoDB 1.19.4, Memcached 3.2.0, Solr 2.8.1 and Composer 2.2.25
are fixed and rebuilt/installed for AMD64. Git, Zip, GD with FreeType/JPEG,
EXIF, MBString, MySQLi, GMP and BCMath are retained.

The image keeps the official FPM entrypoint, `/var/www/html`, port 9000,
www-data UID/GID 33 and SIGQUIT. A FastCGI web server such as Nginx is required.

## Verification and scope

`test.sh` uses isolated containers with no host mounts, external networking
or published ports. It verifies ELF x86-64, source equality, unchanged patched
PHP binaries, non-root FPM requests, repeated same-worker fatal requests,
OOM immediate exit and worker replacement, C-level disabled upload progress,
all extension versions/functions and Composer.

The native AMD64 workflow tests Phalcon 3 and 4 separately. It does not use
registry credentials, publish images, or deploy application services.
Phalcon 4 has not been accepted as a drop-in runtime for a Phalcon 3 application.

OOM terminates a worker immediately without running PHP shutdown callbacks.
Session upload progress is disabled at C level, including when INI tries to
re-enable it. This is the official *minimal EOL mitigation*, not comprehensive
security maintenance for all PHP, Debian, Phalcon or extension issues.

See [PHP_PATCH_PROVENANCE.md](PHP_PATCH_PROVENANCE.md),
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and
[PHALCON_LICENSE.txt](PHALCON_LICENSE.txt).
