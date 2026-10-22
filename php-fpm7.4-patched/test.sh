#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/php74-tests.log" python3 "$ROOT/tests/acceptance.py" "${PHP74_IMAGE:-php74-fpm-patched:7.4.33-php2shell-712e60f9edfd}"
