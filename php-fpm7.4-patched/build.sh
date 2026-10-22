#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$ROOT/fetch-inputs.py"
if [ -z "${PLATFORM:-}" ]; then
    case "$(docker info --format '{{.Architecture}}')" in
        arm64|aarch64) PLATFORM=linux/arm64 ;;
        amd64|x86_64) PLATFORM=linux/amd64 ;;
        *) echo "Set PLATFORM to a supported Linux platform" >&2; exit 1 ;;
    esac
fi
exec python3 "$ROOT/scripts/logged-run.py" "$ROOT/reports/php74-build.log" docker build --progress=plain --platform="${PLATFORM}" -t "${PHP74_IMAGE:-php74-fpm-patched:7.4.33-php2shell-712e60f9edfd}" "$ROOT"
