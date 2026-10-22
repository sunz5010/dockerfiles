# Patch provenance

- PHP 7.4.33 release: <https://www.php.net/distributions/php-7.4.33.tar.xz>
- Release SHA256: `924846abf93bc613815c55dd3f5809377813ac62a9ec4eb3778675b82a27b927`, matching the historical official Docker recipe.
- Official complete security patch: <https://github.com/php/php-src/commit/712e60f9edfd03f0960fc4fc3c2c375f42b90aa2>
- Patch SHA256: `5fe57ca6ee96d59b36c6e0ca842843c50884f177bef1e85234cf669b577f5e48`.
- Official branch checked: `PHP-7.4-CVE-2026-109618-109619`; builds use the pinned patch, not a mutable branch.
- Official Docker recipe/helpers: <https://github.com/docker-library/php/tree/b9f17156020c3aef71df681b27684533529347a7/7.4/bullseye/fpm>.

The official branch reports 7.4.34-dev. This build applies its exact security commit to the verified 7.4.33 release, preserving the requested version. The patch changes 17 files, applies with `--fuzz=0`, and all 17 complete resulting files match the official commit. The independently recorded expected hashes are in `official-source-files.sha256`, checked again by the acceptance script.

## Advisory mapping

- **CVE-2026-109618**: [GHSA-w8hw-w9fx-j79w](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w). The official EOL mitigation hard-exits allocator/overflow failures, hardens concat VM and input allocation behavior, avoiding unsafe OOM bailout cleanup.
- **CVE-2026-109619**: [GHSA-6wmf-4rv5-p3rp](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp). The patch resets request-owned handler/exception/object, SAPI/HTTP/module/llist state and disables the early session upload-progress path.

The entire official patch is applied; it was not reduced to an INI toggle. Both CLI and FPM, headers and development tools are compiled and installed together. `/usr/src/php.tar.xz` contains the patched source for extension helpers. `/usr/local/share/php2shell/` records the patch, commit and source-file hashes inside the image.

## Base and compatibility

The Dockerfile retains the original official Debian Bullseye FPM recipe and configure options. The base is pinned by manifest digest. Removed live-repository packages are served from Debian's official EOL archives. APT signature verification stays enabled; only frozen archive metadata expiry is disabled.

PEAR and PECL channel refreshes use their explicit working official URLs rather than the defunct doc.php.net channel. Original helpers are vendored with immutable source URLs and hashes in `sources.lock.json`.

Rebuildable inputs are locked, but the output is not claimed bit-for-bit reproducible: compilation timestamps, image creation metadata, and PEAR channel metadata may vary. No claim of ongoing Bullseye or PHP 7.4 security maintenance is made.

## Verification limits

The official security commit adds no CVE-specific PHPT. Acceptance combines exact complete source equality, binary and image identity, isolated OOM/FPM request-lifecycle checks, and selected official PHP tests. It is not a complete RCE proof or an audit of every application/extension lifecycle. The minimal EOL mitigation differs from supported PHP 8 soft-OOM semantics; see README for application-visible behavior changes.

Fresh build and test evidence is generated in ignored `reports/` and uploaded as CI artifacts per architecture. Historical ARM64 evidence is summarized in `VALIDATION.md`; it must not be treated as AMD64 verification.
