<?php
function goodbye($customer) {
    echo "Good bye, $customer!\n";
}

class Supermarket {
    public $greet = 'goodbye';
    public $customer = 'dream';
    function __destruct() {
        call_user_func($this->greet, $this->customer);
    }
}
?>