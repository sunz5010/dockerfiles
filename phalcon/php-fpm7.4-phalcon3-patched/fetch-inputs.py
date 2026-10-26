#!/usr/bin/env python3
"""Prepare the Docker build context from immutable, SHA256-locked inputs."""
import hashlib
import json
from pathlib import Path
import sys
import urllib.request


root = Path(__file__).resolve().parent
offline = sys.argv[1:] == ['--offline']
if sys.argv[1:] and not offline:
    sys.exit('Usage: fetch-inputs.py [--offline]')
for name, spec in json.loads((root / 'sources.lock.json').read_text()).items():
    path = root / name
    if path.exists():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != spec['sha256']:
            sys.exit('Checksum mismatch; refusing to replace existing input: ' + name)
        print('VERIFIED', name)
        continue
    if offline:
        sys.exit('Missing input: ' + name + '; run without --offline to download')
    if not spec['url'].startswith('https://'):
        sys.exit('HTTPS source required: ' + name)
    with urllib.request.urlopen(spec['url'], timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != spec['sha256']:
        sys.exit('Downloaded checksum mismatch: ' + name)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.download')
    temporary.write_bytes(data)
    temporary.replace(path)
    if path.name.startswith('docker-php-'):
        path.chmod(0o755)
    print('DOWNLOADED+VERIFIED', name)
