#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/phalcon74-tests.log" \
    python3 "$ROOT/tests/acceptance.py" \
    "${PHALCON74_IMAGE:-phalcon74-patched:4.1.1-php7.4.33-php2shell-arm64}"
