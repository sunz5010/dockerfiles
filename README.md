# dockerfiles

- [PHP 7.4.33-FPM PHP2Shell patched base](php-fpm7.4-patched/): pinned official EOL mitigation, source locks, isolated tests and native arm64/amd64 CI. Published AMD64 base is used by both Phalcon recipes below.
- [Phalcon 3.4.5 / patched PHP 7.4.33 FPM — AMD64](phalcon/php-fpm7.4-phalcon3-patched/): legacy Phalcon 3 APIs with a documented PHP 7.4 compatibility backport.
- [Phalcon 4.1.1 / patched PHP 7.4.33 FPM — AMD64](phalcon/php-fpm7.4-patched/): upstream Phalcon 4.1.1, separately built and validated.
- [WordPress / patched PHP 7.4 FPM — AMD64](wordpress/php-fpm7.4-patched/): WordPress PHP extensions on the Phalcon 4 patched base, with MongoDB 1.19.4.

Phalcon 3 and 4 are different application APIs; choose the matching recipe.
Both Phalcon recipes default to Linux AMD64 (`uname -m` = `x86_64`). Their
native AMD64 workflow builds/tests only and does not publish to Docker Hub or
deploy services. Published image references and exact validation scope are in
each recipe's README and VALIDATION documents.
