#!/bin/sh
# Read-only checks against a running AMD64 PHP-FPM container on this Docker host.
# Does not trigger OOM, modify files, restart workers, or send application requests.
set -eu
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PHP_FPM_CONTAINER_ID" >&2
    exit 2
fi
CID=$1
printf 'Container image reference: '
docker inspect --type container --format '{{.Config.Image}}' "$CID"
docker exec -i "$CID" sh -eu <<'CONTAINER_CHECK'
printf '\nChecking accepted PHP/FPM binaries, running FPM master and official patch:\n'
sha256sum -c - <<'HASHES'
2edf25689ff9dacd129c341cc07ba0ead1f21a1fae82ebd06b606ee9890e21f4  /usr/local/bin/php
187a82cc0dd6eba65cab8bc9b593d3301e247b0adb062bf799be8f042a0c3132  /usr/local/sbin/php-fpm
5fe57ca6ee96d59b36c6e0ca842843c50884f177bef1e85234cf669b577f5e48  /usr/local/share/php2shell/security.patch
HASHES
expected_commit=712e60f9edfd03f0960fc4fc3c2c375f42b90aa2
actual_commit=$(cat /usr/local/share/php2shell/commit)
if [ "$actual_commit" != "$expected_commit" ]; then
    echo 'FAIL: official mitigation commit marker mismatch' >&2
    exit 1
fi
php -r '
if (PHP_VERSION !== "7.4.33" || Phalcon\Version::get() !== "3.4.5") {
    fwrite(STDERR, "FAIL: unexpected PHP/Phalcon version\n"); exit(1);
}
if ((bool) ini_get("session.upload_progress.enabled")) {
    fwrite(STDERR, "FAIL: unexpected CLI upload progress setting\n"); exit(1);
}
echo "PHP ", PHP_VERSION, "; Phalcon ", Phalcon\Version::get(), "; CLI upload progress Off\n";
'
master_executable=$(readlink /proc/1/exe)
case "$master_executable" in
    */qemu-*)
        echo 'PARTIAL: on-disk fingerprints match, but PID 1 is a QEMU emulator.'
        echo 'Run this script on the native x86_64 EC2 host to verify the running FPM master.'
        exit 2
        ;;
esac
printf '%s\n' '187a82cc0dd6eba65cab8bc9b593d3301e247b0adb062bf799be8f042a0c3132  /proc/1/exe' | sha256sum -c -
printf 'PASS: binaries and running FPM master match the published, mitigation-tested AMD64 build.\n'
printf 'This identity check relies on the published build acceptance evidence; it is not an exploit test.\n'
CONTAINER_CHECK
