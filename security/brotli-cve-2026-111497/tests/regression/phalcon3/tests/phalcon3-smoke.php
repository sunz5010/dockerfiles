<?php
// Exercise the Phalcon 3 APIs and native paths affected by the PHP 7.4 port.
function check($condition, $message) {
    if (!$condition) {
        throw new RuntimeException($message);
    }
}

check(Phalcon\Version::get() === '3.4.5', 'Phalcon version');
$di = new Phalcon\Di\FactoryDefault();
check($di instanceof Phalcon\DiInterface, 'Legacy DI interface');
foreach (['Phalcon\Mvc\Collection', 'Phalcon\Mvc\Collection\Manager',
          'Phalcon\Session\Adapter', 'Phalcon\Session\AdapterInterface',
          'Phalcon\Cache\Backend\Libmemcached'] as $class) {
    check(class_exists($class) || interface_exists($class), $class);
}

class LocalConfig extends Phalcon\Config {}
$config = new LocalConfig(['db' => ['host' => 'localhost']]);
check($config->db->host === 'localhost', 'Inherited config property');
$router = new Phalcon\Mvc\Router(false);
$router->add('/items/{id:[0-9]+}', ['controller' => 'items', 'action' => 'show']);
$router->handle('/items/42');
check($router->wasMatched() && $router->getParams()['id'] === '42', 'PCRE router');

$acl = new Phalcon\Acl\Adapter\Memory();
$acl->setDefaultAction(Phalcon\Acl::DENY);
$acl->addRole(new Phalcon\Acl\Role('reader'));
$acl->addResource(new Phalcon\Acl\Resource('novel'), ['view', 'edit']);
$acl->allow('reader', 'novel', 'view');
check($acl->isAllowed('reader', 'novel', 'view'), 'Legacy ACL allow');
check(!$acl->isAllowed('reader', 'novel', 'edit'), 'Legacy ACL deny');

// PHP view loading exercises the ported zend stream-open/include path.
$directory = '/tmp/phalcon3-view-' . getmypid() . '/';
mkdir($directory);
file_put_contents($directory . 'hello.phtml', 'Hello <?= htmlspecialchars($name, ENT_QUOTES, "UTF-8") ?>');
try {
    $view = new Phalcon\Mvc\View\Simple();
    $view->setDI($di);
    $view->setViewsDir($directory);
    check($view->render('hello', ['name' => '<reader>']) === 'Hello &lt;reader&gt;', 'PHP view include');
} finally {
    unlink($directory . 'hello.phtml');
    rmdir($directory);
}
echo 'phalcon3-smoke-ok';
