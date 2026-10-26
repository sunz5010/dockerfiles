#!/bin/sh
set -eu
# This standalone recipe is stored outside its upstream Git repository.
export BUILDX_GIT_INFO=0
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PLATFORM=${PLATFORM:-linux/amd64}
if [ "$PLATFORM" != linux/amd64 ]; then
    echo "This package supports linux/amd64 only." >&2
    exit 1
fi
python3 "$ROOT/fetch-inputs.py"
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/phalcon74-build.log" \
    docker build --progress=plain --platform="$PLATFORM" \
    --build-arg "PHP_BASE_IMAGE=${PHP_BASE_IMAGE:-luofofo/php-fpm7.4-patched@sha256:d466e418826fb80950063e248863954908ea99f42952b24708e08b949788acb7}" \
    -t "${PHALCON74_IMAGE:-phalcon3-php74-patched:3.4.5-php7.4.33-php2shell-20261026-r1-amd64}" "$ROOT"
