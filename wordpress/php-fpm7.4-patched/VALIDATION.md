# WordPress patched PHP 7.4 AMD64 validation

Published and verified on 2026-10-27.

- Image: `luofofo/wordpress-phalcon-php-fpm7.4:4.1.1-php7.4.33-php2shell-20261027-mongo1.19.4-amd64`.
- Digest: `sha256:cdbc0ff08710f331c382e91b82ad0b1fea29e1839f759df21474b87c1acf173c`.
- Base: `luofofo/phalcon-php-fpm7.4-patched@sha256:6bc986f6be9679502391df257ab950c7980ee88ce1f20e87667be50389de409c`.
- Build source: [commit 271d3a1](https://github.com/sunz5010/dockerfiles/commit/271d3a13eafd113bb1bed5366fa2ff0d57a07177).

The recipe was subsequently moved to this directory without changing any
Dockerfile bytes. The published artifact and its digest remain the same.

## Accepted checks

- All PHP module names from the previous WordPress `latest` image are retained.
- Compared with the earlier patched WordPress review, all APT package versions
  are identical; the only PHP extension version change is MongoDB 1.20.1 to 1.19.4.
- Imagick PNG thumbnail/JPEG, GD FreeType/PNG/JPEG, ZIP create/read,
  BCMath/MySQLi initialization and OPcache settings: PASS in CLI and FPM.
- Ghostscript PDF rendering to a 64x64 PNG, including pixel/dimension checks: PASS.
- All five MongoDB integer/string read-preference modes under E_ALL with
  warnings promoted to exceptions: PASS in CLI and FPM.
- PHP CLI/FPM binaries and all 17 official patched source hashes match the
  accepted mitigation base. CLI/FPM lifecycle, OOM exit/worker replacement and
  C-level disabled session upload progress: PASS.
- EntryPoint, command, workdir, FPM port, user and stop signal match old `latest`.
- Anonymous pull and full acceptance against the remote digest: PASS.
- Old `latest` remains at `sha256:342d089aac983a40acb42b9c306d9a80ad6db5fa5bab25ce36c83e54b12022d7`.

## Scope

The release was built and tested as AMD64 under QEMU on an ARM64 Docker daemon.
The Phalcon base has separate native AMD64 CI evidence. These are runtime
checks; no production WordPress site, plugins or application database were
provided or deployed.

The base contains PHP's official minimal EOL mitigation commit
`712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`. This does not constitute ongoing
security maintenance for every PHP, Debian, Phalcon or extension issue.
