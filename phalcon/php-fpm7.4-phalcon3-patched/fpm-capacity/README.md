# Phalcon 3.4.5: restore FPM capacity

This overlay changes exactly two lines in `/usr/local/etc/php-fpm.d/www.conf`:

- `pm.max_children`: **5 → 30**
- `pm.max_spare_servers`: **3 → 20**

It uses the digest-pinned 2026-10-29 Phalcon **3.4.5** image. PHP 7.4.33,
MongoDB 1.19.4, Brotli 1.0.10, all previous security fixes, binaries, packages,
PHP settings, image labels and startup configuration are inherited unchanged.
No Phalcon 4 or WordPress image is modified. Existing tags are preserved.

From the repository root:

```sh
docker build --platform linux/amd64 \
  -t phalcon3-fpm-capacity:20261108 \
  phalcon/php-fpm7.4-phalcon3-patched/fpm-capacity
python3 phalcon/php-fpm7.4-phalcon3-patched/fpm-capacity/verify.py \
  phalcon3-fpm-capacity:20261108
```

Verification uses isolated containers without external networking or published
ports. It checks every exported filesystem entry, verifies that only the two
specified settings changed, confirms unchanged image configuration/base layers,
and checks PHP/Phalcon/MongoDB/Brotli versions, effective FPM settings and startup.
The export is streamed without storing a full image archive.

The image targets **linux/amd64**, matching the existing production image.
Building or publishing it does not update any server or Swarm service.
