# Phalcon 4.1.1 / PHP 7.4.33 patched FPM

This separate recipe uses our published PHP 7.4 PHP2Shell mitigation base:

```dockerfile
FROM luofofo/php-fpm7.4-patched:7.4.33-php2shell-20261022-712e60f9edfd-arm64@sha256:df302e995c224f019b64ac33324fd74ae1a7acd4724d6881effd33c5ccf410d0
```

The published base currently supports **linux/arm64 only**. The original
[`../php-fpm7.4/Dockerfile`](../php-fpm7.4/Dockerfile) is retained separately.
This directory does not publish a Phalcon image to Docker Hub automatically.

## Published image

Docker Hub: [luofofo/phalcon-php-fpm7.4-patched](https://hub.docker.com/r/luofofo/phalcon-php-fpm7.4-patched).
The published image supports **linux/arm64 only**.

```sh
docker pull luofofo/phalcon-php-fpm7.4-patched:4.1.1-php7.4.33-php2shell-20261022-arm64
```

To pin this Phalcon image in a downstream Dockerfile:

```dockerfile
FROM luofofo/phalcon-php-fpm7.4-patched@sha256:d86c498879b60862aef8d9559be13364ca19e963117f9c675e84e61a60e24d12
```

Release source commit: `2c57b2f011525b4426b14ba438785189c9019cd1`.
Remote digest equality, anonymous pull and acceptance by remote digest passed.

## Build and test

Requirements: Docker with BuildKit, Python 3 and network access for verified
source downloads and Debian archive packages. Run from this directory:

```sh
./build.sh
./test.sh
```

Default local image: `phalcon74-patched:4.1.1-php7.4.33-php2shell-arm64`.
Set `PHALCON74_IMAGE` to use another local tag. Build and acceptance evidence is
written to ignored `reports/`.

For a direct Docker build, prepare the complete context first:

```sh
python3 fetch-inputs.py
docker build --platform=linux/arm64 -t phalcon74-patched:local .
PHALCON74_IMAGE=phalcon74-patched:local ./test.sh
```

Downloaded sources are SHA256-locked in `sources.lock.json` and `SHA256SUMS`,
and are excluded from Git. `python3 fetch-inputs.py --offline` verifies an
already prepared context. The base image uses Debian's signed Bullseye archive
repositories; this recipe inherits that configuration.

## Compatibility changes

- Pin Phalcon's official v4.1.1 source commit, replacing the removed
  `4.1.1-release` branch, and explicitly select its 64-bit build on ARM64.
- Pin PSR 1.2.0, MongoDB 1.20.1, Memcached 3.2.0, Solr 2.8.1 and Composer 2.2.25.
  Install a verified Composer PHAR instead of executing a remote installer.
- Preserve Git, Zip, GD with FreeType/JPEG, EXIF, MBString, MySQLi, GMP and BCMath.
- Leave the Solr build directory before removing it, and prepare PEAR's cache
  directory before clearing the cache.

## Validation and scope

`test.sh` checks the 17 official patched PHP source hashes, PHP/FPM/tool versions,
non-root FPM requests, repeated fatal-error requests, immediate OOM exit and
worker replacement, and disabled session upload progress. It also exercises
Phalcon DI/Escaper, MongoDB BSON, Memcached initialization, SolrQuery, GD PNG,
Zip, MySQLi initialization, GMP, BCMath, extension versions and Composer.
No external MongoDB, Memcached, Solr or application fixtures are required.
See [VALIDATION.md](VALIDATION.md) for the recorded build result.

The base contains PHP's official minimal EOL mitigation commit
`712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`. OOM terminates a worker immediately,
and session upload progress is disabled at C level. This is not comprehensive
security maintenance for end-of-life PHP, Debian, Phalcon or its extensions.
Base patch attribution: [PATCH_PROVENANCE.md](../../php-fpm7.4-patched/PATCH_PROVENANCE.md).
