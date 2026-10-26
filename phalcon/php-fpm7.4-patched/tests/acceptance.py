#!/usr/bin/env python3
"""Isolated CLI/FPM lifecycle checks; no published ports or external services."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
IMAGE = sys.argv[1]
PREFIX = 'phalcon74'
REPORT = ROOT / 'reports' / (PREFIX + '-acceptance.json')
NAME = 'php2shell-test-' + uuid.uuid4().hex[:12]
REPORT.parent.mkdir(parents=True, exist_ok=True)
results = []


def run(args, data=None, expected=0):
    p = subprocess.run(['docker'] + args, input=data, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=180)
    results.append(dict(command=['docker'] + args, exit_code=p.returncode, output=p.stdout))
    if expected is not None and p.returncode != expected:
        raise AssertionError(p.stdout)
    return p.stdout


def put(path, content):
    run(['exec', '-i', NAME, 'sh', '-c', 'cat > ' + path], content)


FCGI = r'''<?php
function rec($t,$v) { return pack('CCnnCC',1,$t,1,strlen($v),0,0).$v; }
function nv($s) { $n=strlen($s); return ($n<128?chr($n):pack('N',$n|0x80000000)); }
$f=fsockopen('127.0.0.1',9000,$errno,$errstr,5); stream_set_timeout($f,10);
$params=['SCRIPT_FILENAME'=>'/var/www/html/'.$argv[1], 'REQUEST_METHOD'=>'GET',
 'SERVER_PROTOCOL'=>'HTTP/1.1','SERVER_NAME'=>'localhost','SERVER_PORT'=>'80',
 'REQUEST_URI'=>'/'.$argv[1], 'GATEWAY_INTERFACE'=>'CGI/1.1'];
if (isset($argv[2])) $params['PHP_VALUE']=$argv[2];
$body='';
if (isset($argv[3])) {
 $body=file_get_contents($argv[3]); $params['REQUEST_METHOD']='POST';
 $params['CONTENT_TYPE']='multipart/form-data; boundary=testboundary';
 $params['CONTENT_LENGTH']=(string)strlen($body);
 $params['HTTP_COOKIE']='PHPSESSID=php2shelltest';
}
$p=''; foreach ($params as $k=>$v) $p.=nv($k).nv($v).$k.$v;
fwrite($f,rec(1,pack('nCxxxxx',1,0)).rec(4,$p).rec(4,'').rec(5,$body).rec(5,''));
function exact($f,$n) { $s=''; while(strlen($s)<$n && !feof($f)) { $b=fread($f,$n-strlen($s)); if($b==='')break; $s.=$b; } return $s; }
while(!feof($f)) { $h=exact($f,8); if(strlen($h)<8)break;
 $a=unpack('Cv/Ct/nid/nlen/Cpad/Creserved',$h); $b=exact($f,$a['len']);
 if($a['pad'])exact($f,$a['pad']); if($a['t']==6)echo $b;
 if($a['t']==7)fwrite(STDERR,$b); if($a['t']==3)break;
}
fclose($f);
'''

try:
    inspect = json.loads(run(['image', 'inspect', IMAGE]))[0]
    daemon_arch = run(['info', '--format', '{{.Architecture}}']).strip()
    assert 'x86-64' in run(['run', '--rm', '--platform', 'linux/amd64', '--network', 'none', IMAGE, 'file', '/usr/local/bin/php'])
    run(['run', '--platform', 'linux/amd64', '-d', '--name', NAME, '--network', 'none', '--memory', '512m',
         '--pids-limit', '64', IMAGE, 'sleep', '600'])
    for args in [['php', '-v'], ['php-fpm', '-v'], ['phpize', '--version'],
                 ['php-config', '--configure-options'], ['php', '-m'], ['php-fpm', '-t']]:
        run(['exec', NAME] + args)
    assert run(['exec', NAME, 'php', '-r', 'echo PHP_VERSION;']).strip() == '7.4.33'
    assert run(['exec', NAME, 'cat', '/usr/local/share/php2shell/commit']).strip() == '712e60f9edfd03f0960fc4fc3c2c375f42b90aa2'
    assert run(['exec', NAME, 'php', '-r', 'echo (int)ini_get("session.upload_progress.enabled");']).strip() == '0'
    run(['exec', NAME, 'docker-php-source', 'extract'])
    run(['exec', '-w', '/usr/src/php', NAME, 'sha256sum', '-c', '/usr/local/share/php2shell/source-files.sha256'])
    actual_sources = run(['exec', NAME, 'cat', '/usr/local/share/php2shell/source-files.sha256'])
    assert actual_sources == (ROOT / 'official-source-files.sha256').read_text()
    assert inspect['Architecture'] == 'amd64' and inspect['Os'] == 'linux'
    hashes = run(['exec', NAME, 'sha256sum', '/usr/local/bin/php', '/usr/local/sbin/php-fpm',
                  '/usr/local/bin/phpize', '/usr/local/bin/php-config'])
    assert hashes == (ROOT / 'base-binaries.sha256').read_text(), 'PHP binaries differ from the accepted patched base'
    put('/tmp/oom.php', '<?php register_shutdown_function(function(){file_put_contents("/tmp/shutdown-ran","yes");}); str_repeat("x",64*1024*1024);')
    oom = run(['exec', NAME, 'php', '-n', '-d', 'memory_limit=8M', '/tmp/oom.php'], expected=1)
    assert 'Allowed memory size' in oom
    run(['exec', NAME, 'test', '!', '-e', '/tmp/shutdown-ran'])
    put('/tmp/fcgi.php', FCGI)
    put('/tmp/test-fpm.conf', '''[global]
daemonize=no
error_log=/tmp/fpm.log
[www]
user=www-data
group=www-data
listen=127.0.0.1:9000
pm=static
pm.max_children=1
catch_workers_output=yes
clear_env=no
''')
    put('/var/www/html/health.php', '<?php header("Content-Type: application/json"); echo json_encode(["version"=>PHP_VERSION,"pid"=>getmypid(),"uid"=>posix_geteuid(),"ok"=>array_sum([1,2,3])===6,"extensions"=>get_loaded_extensions()]);')
    put('/var/www/html/fatal.php', '<?php set_error_handler(function(){return false;}); echo "producer:".getmypid(); throw new Exception("lifecycle regression");')
    put('/var/www/html/oom.php', '<?php ini_set("memory_limit","8M"); str_repeat("x",64*1024*1024);')
    put('/var/www/html/upload.php', '<?php echo "upload-ok:".getmypid();')
    run(['exec', NAME, 'sh', '-c', 'mkdir -p /tmp/session-progress; chmod 777 /tmp/session-progress'])
    run(['exec', '-d', NAME, 'php-fpm', '-F', '-y', '/tmp/test-fpm.conf'])
    time.sleep(1)

    def fcgi(script, ini=None, body=None):
        args = ['exec', NAME, 'php', '/tmp/fcgi.php', script]
        if ini is not None: args.append(ini)
        if body is not None: args.append(body)
        return run(args)

    def health(ini=None):
        s = fcgi('health.php', ini)
        d = json.loads(s[s.index('{'):])
        assert d['ok'] and d['uid'] == 33 and d['version'] == '7.4.33'
        return d

    # A library compatibility regression must fail on E_DEPRECATED, not hide it.
    put('/var/www/html/legacy-readpreference.php', (ROOT / 'tests/legacy-readpreference.php').read_text())
    assert 'legacy-readpreference-ok' in run(['exec', NAME, 'php', '/var/www/html/legacy-readpreference.php'])
    assert 'legacy-readpreference-ok' in fcgi('legacy-readpreference.php')

    first = health()
    for _ in range(5):
        assert 'producer:' + str(first['pid']) in fcgi('fatal.php')
        assert health('date.timezone=Invalid/Timezone')['pid'] == first['pid']
    fcgi('oom.php')
    time.sleep(1)
    after = health()
    assert after['pid'] != first['pid']
    put('/tmp/multipart', '--testboundary\r\nContent-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\nprobe\r\n--testboundary\r\nContent-Disposition: form-data; name="f"; filename="t.txt"\r\nContent-Type: text/plain\r\n\r\nhello\r\n--testboundary--\r\n')
    upload = fcgi('upload.php', 'session.upload_progress.enabled=1\nsession.upload_progress.cleanup=0\nsession.save_path=/tmp/session-progress', '/tmp/multipart')
    assert 'upload-ok:' in upload
    assert run(['exec', NAME, 'sh', '-c', 'find /tmp/session-progress -type f']).strip() == ''
    assert health()['pid'] == after['pid']
    run(['exec', NAME, 'cat', '/tmp/fpm.log'])
    if PREFIX.startswith('phalcon'):
        for ext in ['phalcon', 'psr', 'mongodb', 'memcached', 'solr', 'gd', 'exif', 'mbstring', 'zip', 'mysqli', 'gmp', 'bcmath']:
            run(['exec', NAME, 'php', '--ri', ext])
        run(['exec', NAME, 'php', '-r', 'if(Phalcon\\Version::get()!=="4.1.1")exit(1); $di=new Phalcon\\Di\\FactoryDefault(); echo "phalcon-ok\\n"; if(!extension_loaded("mongodb")||!class_exists("SolrClient")||!class_exists("Memcached")||gmp_strval(gmp_add(2,3))!=="5"||bcadd("2","3")!=="5")exit(2); $im=imagecreatetruecolor(2,2); imagedestroy($im);'])
        put('/var/www/html/extension-smoke.php', r'''<?php
if (Phalcon\Version::get() !== "4.1.1") exit(1);
$di = new Phalcon\Di\FactoryDefault();
$esc = new Phalcon\Escaper();
if ($esc->escapeHtml("<b>") !== "&lt;b&gt;") exit(2);
$encoded = MongoDB\BSON\fromPHP(["x"=>42]);
if (MongoDB\BSON\toPHP($encoded)->x !== 42) exit(3);
$cache = new Memcached(); $cache->setOption(Memcached::OPT_CONNECT_TIMEOUT, 100);
$solr = new SolrQuery(); $solr->setQuery("hello");
if ($solr->getQuery() !== "hello") exit(4);
$db = mysqli_init();
$zip = new ZipArchive(); if($zip->open("/tmp/smoke.zip", ZipArchive::CREATE)!==true)exit(5);
$zip->addFromString("hello.txt","hello"); $zip->close();
$im=imagecreatetruecolor(2,2); ob_start(); imagepng($im); $png=ob_get_clean(); imagedestroy($im);
if(substr($png,1,3)!=="PNG" || gmp_strval(gmp_add(2,3))!=="5" || bcadd("2","3")!=="5")exit(6);
echo "extension-smoke-ok";
''')
        assert 'extension-smoke-ok' in fcgi('extension-smoke.php')
        assert set(['phalcon','mongodb','memcached','solr','gd','exif','mbstring','zip','mysqli','gmp','bcmath','psr']).issubset(set(health()['extensions']))
        assert '2.2.25' in run(['exec', NAME, 'composer', '--version'])
        expected_versions = {'psr': '1.2.0', 'mongodb': '1.19.4', 'memcached': '3.2.0', 'solr': '2.8.1', 'phalcon': '4.1.1'}
        for extension, version in expected_versions.items():
            assert run(['exec', NAME, 'php', '-r', 'echo phpversion("'+extension+'");']).strip() == version
    report = dict(status='PASS', image_id=inspect['Id'], repo_digests=inspect['RepoDigests'],
                  architecture=inspect['Architecture'], binary_hashes=hashes,
                  daemon_architecture=daemon_arch,
                  execution='native AMD64' if daemon_arch in ('amd64', 'x86_64') else 'AMD64 under cross-architecture execution',
                  scope='Official minimal EOL mitigation; source equality, OOM immediate exit, same-worker fatal/early diagnostic, disabled upload lifecycle, CLI/FPM smoke. Not comprehensive exploit or sanitizer proof.',
                  first_worker=first, replacement_worker=after)
except Exception as e:
    report = dict(status='FAIL', error=str(e))
finally:
    run(['rm', '-f', NAME], expected=None)
    report.update(time=datetime.datetime.now(datetime.timezone.utc).isoformat(), results=results)
    REPORT.write_text(json.dumps(report, indent=2))
    print(str(REPORT), report['status'])
sys.exit(0 if report['status'] == 'PASS' else 1)
