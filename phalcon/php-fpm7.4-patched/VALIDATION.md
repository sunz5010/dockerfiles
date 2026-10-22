# Recorded validation

Date: 2026-10-22. Platform: native Linux ARM64 in the isolated project VM.

- Build: PASS, exit 0.
- CLI/FPM lifecycle and extension acceptance: PASS, exit 0.
- Local image: `phalcon74-patched:4.1.1-php7.4.33-php2shell-arm64`.
- Image descriptor: `sha256:d86c498879b60862aef8d9559be13364ca19e963117f9c675e84e61a60e24d12`.
- Published base index: `sha256:df302e995c224f019b64ac33324fd74ae1a7acd4724d6881effd33c5ccf410d0`.
- PHP CLI, FPM, phpize and php-config binary SHA256 values match the accepted
  published base exactly. The 17 official patched source files also match.
- Required versions: PHP 7.4.33; Phalcon 4.1.1; PSR 1.2.0; MongoDB 1.20.1;
  Memcached 3.2.0; Solr 2.8.1; Composer 2.2.25.

Acceptance exercises non-root FPM requests; repeated fatal/early-diagnostic
requests in the same worker; OOM hard exit without a PHP shutdown callback;
worker replacement; disabled session upload progress even when requested;
Phalcon DI/Escaper, MongoDB BSON roundtrip, Memcached initialization, SolrQuery,
GD PNG, Zip, MySQLi initialization, GMP and BCMath.

Build output retains two upstream `-Wstringop-overflow` diagnostics in Phalcon
concatenation / PHP smart-string code and a build-time notice that MBString is
already loaded in the base. This validation is not an ASan audit of those
extensions. It does not include external database/cache/search services or
application-specific tests.

The published PHP base separately passed 1006 selected official PHPT cases
with 12 skips and zero failures; those PHPT results belong to the base.
This change was built/tested locally on ARM64 and did not trigger a new cloud
build. AMD64 is not supported by the currently published base.

Full build and acceptance reports are generated in ignored `reports/` by
`./build.sh` and `./test.sh`. A local evidence copy and image archive are retained
in the handoff workspace. No Phalcon image was published to Docker Hub as part
of this source change.
