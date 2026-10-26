#!/bin/sh
set -eu
export BUILDX_GIT_INFO=0
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PLATFORM=${PLATFORM:-linux/amd64}
if [ "$PLATFORM" != linux/amd64 ]; then
    echo "This recipe supports linux/amd64 only." >&2
    exit 1
fi
python3 "$ROOT/fetch-inputs.py"
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/phalcon74-build.log" \
    docker build --progress=plain --platform="$PLATFORM" \
    -t "${PHALCON74_IMAGE:-phalcon74-patched:4.1.1-php7.4.33-php2shell-20261027-mongo1.19.4-amd64}" "$ROOT"
