#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/php74-phpt.log" docker run --rm --network none --memory 768m --pids-limit 128 "${PHP74_IMAGE:-php74-fpm-patched:7.4.33-php2shell-712e60f9edfd}" sh -ec '
docker-php-source extract
cd /usr/src/php
export TEST_PHP_EXECUTABLE=/usr/local/bin/php REPORT_EXIT_STATUS=1 NO_INTERACTION=1
php -n run-tests.php -n -q --show-diff ext/standard/tests/array Zend/tests/generators Zend/tests/exception*.phpt ext/session/tests/session_*basic*.phpt ext/session/tests/session_encode*.phpt ext/session/tests/session_decode*.phpt
'
