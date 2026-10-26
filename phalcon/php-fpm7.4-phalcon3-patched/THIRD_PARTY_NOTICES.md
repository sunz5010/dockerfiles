# Third-party notices

This image is derived from the patched PHP 7.4 FPM recipe and the Phalcon
recipe in https://github.com/sunz5010/dockerfiles/tree/master/phalcon.
It contains PHP, Debian packages, Phalcon, PHP extensions and Composer,
which retain their respective upstream licenses.

Phalcon 3.4.5 source: https://github.com/phalcon/cphalcon/commit/d4e0362207fd2f7bdd26feca0b4271056d52a06a
License: BSD 3-Clause; the complete notice is in PHALCON_LICENSE.txt.
The PHP 7.4 compatibility patch changes generated kernel code for property
scope lookup, PCRE subject arguments and Zend stream-open initialization.
These changes were adapted from official Phalcon 4.1.1 kernel code:
https://github.com/phalcon/cphalcon/tree/dcb2be7acac3856ecba9b1032ddee9270503a614/ext/kernel
Both Phalcon versions use the BSD 3-Clause license. The modified source is
identified by sources.lock.json plus php74-compat.patch, supplied with the
image under /usr/local/share/phalcon3-php74/.

PHP license: /usr/local/share/licenses/php/PHP-LICENSE.txt.
PHP mitigation provenance: PHP_PATCH_PROVENANCE.md in the source package;
the base image records its patch under /usr/local/share/php2shell/.
Debian package copyright/license notices remain under /usr/share/doc/.
