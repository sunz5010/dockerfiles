#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PLATFORM=${PLATFORM:-linux/arm64}
if [ "$PLATFORM" != linux/arm64 ]; then
    echo "The published patched base currently supports linux/arm64 only." >&2
    exit 1
fi
python3 "$ROOT/fetch-inputs.py"
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/phalcon74-build.log" \
    docker build --progress=plain --platform="$PLATFORM" \
    -t "${PHALCON74_IMAGE:-phalcon74-patched:4.1.1-php7.4.33-php2shell-arm64}" "$ROOT"
