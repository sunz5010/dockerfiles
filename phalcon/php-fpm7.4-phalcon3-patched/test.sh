#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/phalcon74-tests.log" \
    python3 "$ROOT/tests/acceptance.py" \
    "${PHALCON74_IMAGE:-phalcon3-php74-patched:3.4.5-php7.4.33-php2shell-20261026-r1-amd64}"
