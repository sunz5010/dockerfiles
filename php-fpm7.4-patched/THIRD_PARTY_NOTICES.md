# Third-party notices

`Dockerfile` is adapted from docker-library/php's PHP 7.4.33 Bullseye FPM recipe. The five `docker-php-*` helpers are unmodified official files from commit `b9f17156020c3aef71df681b27684533529347a7`. The upstream MIT license is retained in `licenses/docker-library-php-MIT.txt`.

`security.patch` is the complete official PHP source commit `712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`. The downloaded PHP release and patch affect PHP and Zend sources. Their upstream license texts are retained in `licenses/PHP-LICENSE.txt` and `licenses/Zend-LICENSE.txt`, and the complete source distribution preserves its own notices.

Source URLs and fixed SHA256 hashes are recorded in `sources.lock.json`. Upstream sources and advisory attribution are recorded in `PATCH_PROVENANCE.md`.

`pear-channel.xml` and `pecl-channel.xml` are official channel configuration snapshots from pear.php.net and pecl.php.net, retained byte-for-byte with SHA256 locks.
