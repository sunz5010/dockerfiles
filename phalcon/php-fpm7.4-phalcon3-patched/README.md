# Phalcon 3.4.5 / patched PHP 7.4.33 FPM — AMD64

For existing Phalcon 3 applications that need the patched PHP 7.4 runtime.
This recipe builds **linux/amd64** (Linux `x86_64`) and preserves Phalcon 3
Collection/ODM, Session, Cache and legacy DI interfaces.

## Published image

[Docker Hub](https://hub.docker.com/r/luofofo/phalcon-php-fpm7.4-patched/tags?name=3.4.5)

```sh
docker pull luofofo/phalcon-php-fpm7.4-patched:3.4.5-php7.4.33-php2shell-20261027-mongo1.19.4-amd64
```

The earlier Phalcon 3 ARM64 tags were retired at the user's request. This
recipe and tag target AMD64. Phalcon 4 has a separate recipe at
[`../php-fpm7.4-patched/`](../php-fpm7.4-patched/).


MongoDB 1.19.4 is intentionally pinned for older libraries that pass integer
`ReadPreference::RP_*` modes. CLI and FPM acceptance promote PHP warnings to
exceptions while checking these legacy modes. Existing 2026-10-26 tags are kept
for rollback; no existing tag is overwritten. This is a compatibility pin, not
a claim that older MongoDB libraries or extensions receive current security fixes.

## Build and test

Requires Docker/buildx, Python 3 and network access for verified sources and
Debian archive packages. On AMD64, run from this directory:

```sh
./build.sh
./test.sh
```

On ARM64, AMD64 execution support (such as QEMU) must be configured first.
All downloaded archives are SHA256-locked in `sources.lock.json` and
`SHA256SUMS`, excluded from Git, and verified again by the Dockerfile.
`python3 fetch-inputs.py --offline` checks a prepared build context.

The base is the published, digest-pinned AMD64 PHP 7.4.33 mitigation image:
`luofofo/php-fpm7.4-patched@sha256:d466e418826fb80950063e248863954908ea99f42952b24708e08b949788acb7`.
Tests require PHP CLI/FPM/phpize/php-config hashes to match that accepted base.
Changing the base requires independently revalidating the expected hashes.

## Phalcon compatibility backport

Phalcon's official 3.4.x commit
`d4e0362207fd2f7bdd26feca0b4271056d52a06a` reports runtime version 3.4.5.
Its archive SHA256 is
`12b640c47903f0e65c8f0b1b949a35bf616419152041a9c4410061cc79c9c95c`.

`php74-compat.patch` adapts three generated kernel paths for PHP 7.4:
property scope lookup, PCRE `zend_string` arguments, and Zend stream-open
initialization. The implementation is adapted from official Phalcon 4.1.1
kernel code; it does not change PHP's security patch. Its SHA256 is
`a6af3a8cea677405e4ddee12bf538b650915a7f0e439ce69cc5d26ca2d9343eb`,
and it is applied with `--fuzz=0`.

This is a custom compatibility backport, not an official Phalcon 3/PHP 7.4
release or a complete native-extension security audit.

## Included extensions

PSR 1.2.0, MongoDB 1.19.4, Memcached 3.2.0, Solr 2.8.1, Composer 2.2.25,
GD with FreeType/JPEG, EXIF, MBString, Zip, MySQLi, GMP, BCMath, Git and Zip.
The image retains the PHP-FPM entrypoint, `/var/www/html`, port 9000,
www-data UID/GID 33 and SIGQUIT. Nginx or another FastCGI web server is required.

## Validation and scope

`test.sh` runs isolated containers without host mounts, external networking
or published host ports. It verifies the 17 official patched PHP source hashes,
CLI/FPM mitigation lifecycle, all extensions and the Phalcon 3 native paths.
The repository's AMD64 workflow builds and tests Phalcon 3 and 4 separately;
it does not log in to Docker Hub or publish/deploy images.

`sh verify-running.sh CONTAINER_ID` performs read-only fingerprint checks on a
running native AMD64 FPM container. QEMU is explicitly reported as PARTIAL
because `/proc/1/exe` refers to the emulator rather than the FPM executable.
This check depends on trusted build evidence and is not an exploit test.

See [VALIDATION.md](VALIDATION.md), [PHP_PATCH_PROVENANCE.md](PHP_PATCH_PROVENANCE.md),
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [PHALCON_LICENSE.txt](PHALCON_LICENSE.txt).
