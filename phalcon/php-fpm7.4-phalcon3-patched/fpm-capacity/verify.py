#!/usr/bin/env python3
"""Verify a configuration-only overlay in isolated containers; never deploy."""
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import time
import uuid

BASE = 'luofofo/phalcon-php-fpm7.4-patched@sha256:58f811169eb23a1f936e901671ae29f3f75d2b0496fa28584e9d267ae075f6ef'
TARGET = 'usr/local/etc/php-fpm.d/www.conf'
INJECTED = {'etc/hosts', 'etc/hostname', 'etc/resolv.conf'}


def docker(*args):
    return subprocess.check_output(['docker', *args], text=True)


def inspect(image):
    return json.loads(docker('image', 'inspect', image))[0]


def filesystem(container):
    # Stream the export so no full image archive is written to disk.
    process = subprocess.Popen(['docker', 'export', container], stdout=subprocess.PIPE)
    entries = {}
    config = None
    with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
        for member in archive:
            path = member.name.removeprefix('./').rstrip('/')
            if path in INJECTED:
                continue
            digest = None
            if member.isfile():
                stream = archive.extractfile(member)
                checksum = hashlib.sha256()
                chunks = [] if path == TARGET else None
                while True:
                    chunk = stream.read(1024 * 1024)
                    if not chunk:
                        break
                    checksum.update(chunk)
                    if chunks is not None:
                        chunks.append(chunk)
                digest = checksum.hexdigest()
                if chunks is not None:
                    config = b''.join(chunks)
            entries[path] = (member.type.decode('ascii'), member.mode, member.uid,
                             member.gid, member.linkname, digest)
    process.stdout.close()
    assert process.wait() == 0, 'Docker export failed'
    assert config is not None, 'FPM pool configuration missing'
    return entries, config


def main():
    image = sys.argv[1]
    base = inspect(BASE)
    candidate = inspect(image)
    assert candidate['Architecture'] == base['Architecture'] == 'amd64'
    assert candidate['Os'] == base['Os'] == 'linux'
    assert candidate['Config'] == base['Config'], 'Image runtime configuration changed'
    layers = base['RootFS']['Layers']
    assert candidate['RootFS']['Layers'][:-1] == layers, 'Base layers changed'
    containers = []
    try:
        for source in [BASE, image]:
            name = 'phalcon3-fpm-capacity-' + uuid.uuid4().hex[:10]
            docker('create', '--platform', 'linux/amd64', '--network', 'none',
                   '--name', name, source)
            containers.append(name)
        before, old_config = filesystem(containers[0])
        after, new_config = filesystem(containers[1])
        assert set(before) == set(after), 'Filesystem paths changed'
        changed = [path for path in before if before[path] != after[path]]
        assert changed == [TARGET], 'Unexpected filesystem changes: ' + repr(changed)
        assert before[TARGET][:-1] == after[TARGET][:-1], 'Pool file permissions changed'
        for old in [b'pm.max_spare_servers = 3', b'pm.max_children = 5']:
            assert old_config.count(old) == 1, 'Unexpected baseline pool settings'
        expected = old_config.replace(b'pm.max_spare_servers = 3', b'pm.max_spare_servers = 20')
        expected = expected.replace(b'pm.max_children = 5', b'pm.max_children = 30')
        assert new_config == expected, 'Pool configuration has unrelated changes'

        name = containers[1]
        docker('start', name)
        result = subprocess.run(['docker', 'exec', name, 'php-fpm', '-tt'],
                                capture_output=True, text=True, check=True)
        configuration = result.stdout + result.stderr
        for setting, value in [('pm', 'dynamic'), ('pm.start_servers', '2'),
                               ('pm.min_spare_servers', '1'), ('pm.max_children', '30'),
                               ('pm.max_spare_servers', '20')]:
            assert re.search(r'\b' + re.escape(setting) + r' = ' + value + r'\s*$',
                             configuration, re.M), 'Unexpected effective setting: ' + setting
        versions = json.loads(docker('exec', name, 'php', '-r',
            'echo json_encode(["php"=>PHP_VERSION,"phalcon"=>Phalcon\\Version::get(),'
            '"mongodb"=>phpversion("mongodb"),"brotli"=>curl_version()["brotli_version"]]);'))
        assert versions == {'php': '7.4.33', 'phalcon': '3.4.5', 'mongodb': '1.19.4', 'brotli': '1.0.10'}
        ready = False
        for _ in range(20):
            logs = subprocess.run(['docker', 'logs', '--tail', '30', name],
                                  capture_output=True, text=True, check=True)
            if 'ready to handle connections' in logs.stdout + logs.stderr:
                ready = True
                break
            time.sleep(0.25)
        assert ready, 'FPM did not become ready'
        print(json.dumps({'status': 'PASS', 'base': BASE, 'image': image,
                          'image_id': candidate['Id'], 'platform': 'linux/amd64',
                          'verified_filesystem_entries': len(before), 'changed_files': changed,
                          'runtime_config_unchanged': True, 'base_layers_unchanged': True,
                          'versions': versions, 'max_children': 30, 'max_spare_servers': 20,
                          'fpm_ready': ready}, indent=2))
    finally:
        for name in containers:
            subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    main()
