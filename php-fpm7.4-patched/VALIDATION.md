# Validation record

## Original isolated build — 2026-10-22

Platform: native Linux arm64. Full PHP 7.4.33 CLI/FPM image built from the official complete patch.

| Check | Result |
| --- | --- |
| Docker build | PASS |
| Full patched source-file equality to official commit | 17 / 17 PASS |
| CLI/FPM/phpize/php-config and FPM config | PASS |
| Worker UID 33 and FastCGI request smoke | PASS |
| CLI hard OOM, no shutdown callback | PASS |
| FPM hard OOM, worker replacement and healthy next request | PASS |
| Five same-worker fatal / early-INI-diagnostic pairs | PASS |
| Upload-progress C-level disable despite re-enable attempt | PASS |
| Official selected PHPT | 1006 PASS / 12 SKIP / 0 FAIL (1018 total) |

The 12 upstream PHPT skips comprise nine 32-bit-only cases, two unavailable-CGI cases and one unavailable locale. The original recipe disables CGI; FPM is tested separately.

Original ARM64 PHP binary SHA256: `0a2a8e15f6807796e65a29dfe45f9f1a71d59e2404c666031faec1889b8e64b6`.

Original ARM64 FPM binary SHA256: `54ae8634bcc94ccda13f8520d4a3bcc69a178aa825e798f6925de38fb3f5e4d8`.

These hashes identify that historical build; rebuild timestamps can change binary hashes. New test reports must record their own image ID and hashes.

## Repository package

The standalone package was built and tested again on native ARM64 before upload on 2026-10-22: build PASS, lifecycle acceptance PASS, 1006 official PHPT PASS / 12 SKIP / 0 FAIL. The standalone acceptance additionally compares all 17 source hashes directly against the committed official full-file hash manifest. GitHub Actions also builds and tests both arm64 and amd64 natively. A workflow definition is not evidence of a passing run: consult the workflow run and its per-architecture report artifacts.

Validation covers the official minimal EOL mitigation and listed test scope. It is not complete security maintenance, a full extension/application audit, or proof that every possible exploit is blocked.

## Deterministic channel metadata follow-up

A cloud diagnostic run identified invalid XML from the live PECL channel endpoint after PHP compilation/install succeeded. The recipe now uses official checksum-locked local PEAR/PECL XML; a network-disabled channel update probe passed, then the revised ARM64 build, source/lifecycle acceptance and official PHPT passed again (1006 PASS / 12 SKIP / 0 FAIL). A native AMD64 run of the preceding recipe also passed the complete build/test workflow. Consult CI for the final per-architecture results of the current recipe.
