# Phalcon 4.1.1 / PHP 7.4.33 AMD64 validation

Published and verified on 2026-10-26.

- Image: `luofofo/phalcon-php-fpm7.4-patched:4.1.1-php7.4.33-php2shell-20261026-amd64`.
- Manifest digest: `sha256:41cf4be8b17775b60ac128b9b62e0c0afe1f07b077bff66c1aaa474ac74ea436`.
- Platform: linux/amd64 (`x86_64`).
- Base: `luofofo/php-fpm7.4-patched@sha256:d466e418826fb80950063e248863954908ea99f42952b24708e08b949788acb7`.

## Accepted checks

- PHP 7.4.33 and Phalcon 4.1.1; PHP executable is ELF x86-64.
- PHP CLI/FPM/phpize/php-config SHA256 values exactly equal the published,
  independently accepted patched AMD64 base.
- All 17 complete PHP source hashes match official mitigation commit
  `712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`.
- Non-root FPM worker, repeated same-worker fatal/early diagnostic requests,
  immediate CLI OOM exit without PHP shutdown callback, FPM OOM worker
  replacement and C-level disabled session upload progress: PASS.
- Fixed PSR/MongoDB/Memcached/Solr/Phalcon versions; DI/Escaper, BSON,
  Memcached initialization, SolrQuery, GD PNG, Zip, MySQLi initialization,
  GMP, BCMath, extension availability in FPM and Composer: PASS.
- Remote manifest identity equals the accepted image descriptor.
- Anonymous pull with an empty Docker config: PASS.
- Full acceptance against the remote digest after pull: PASS.

The base's selected official PHP regressions previously passed with 1006
PASS, 12 SKIP and 0 FAIL. They are base evidence; the final image acceptance
separately loads and exercises the native extensions and FPM lifecycle.

## Scope

This release build and full local acceptance executed AMD64 binaries under
QEMU in an ARM64 Linux Docker VM. Native AMD64 build/test CI for this recipe
and the separate Phalcon 3 recipe is included in
[the repository workflow](../../.github/workflows/phalcon74-amd64.yml).
CI does not log in to a registry, publish images or deploy services.

Phalcon 4 has not been accepted as a drop-in runtime for a Phalcon 3
application. The existing Phalcon 3 AMD64 image is retained, with its source
recipe at `../php-fpm7.4-phalcon3-patched/`. No application services were changed.

The old `4.1.1-php7.4.33-php2shell-20261022-arm64` tag was retired at the
user's request. No AMD64 tags or `latest` were overwritten.

This is PHP's official minimal EOL mitigation, not comprehensive security
maintenance or a complete exploit/sanitizer proof. GCC emitted stringop-overflow
warnings in generated Phalcon concat code and legacy MBString code, and
installation reported mbstring already loaded; completed runtime tests passed.
These functional checks do not establish the safety of every native path.

Full build/acceptance/push/anonymous-pull/manifest evidence is retained in the
maintainer's ignored `reports/`; CI uploads independent per-job evidence.
