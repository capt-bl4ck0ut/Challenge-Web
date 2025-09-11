<?php
include "_flag.php";

if ($_SERVER["REMOTE_ADDR"] === "127.0.0.1" || $_SERVER["REMOTE_ADDR"] === "::1") {
    if($_POST["mode"] === "write" && isset($_POST["dbkey"]) && isset($_POST["key"])) {
        
        $k1 = md5($_POST["dbkey"]);
        $k2 = md5($_POST["dbkey"].$_POST["key"]);
        $value = base64_encode($flag);

        @file_put_contents("/tmp/api-portal/db/$k1/$k2", $value);
        die("success");
    }
}

$x = $flag;
for($i = 0; $i < 1337; $i++)
    $x = sha1($x);

header("Content-Type: text/plain");


die(<<<EOF
--API Portal Doc--
Endpoint: flag/flag
Method: POST
Parameter: [POST] mode "write" (mandatory)
Parameter: [POST] dbkey
Parameter: [POST] key

Update (dbkey->key)'s value of the Key-Value storage with flag


Fun fact: (sha1 * sha1 * ... sha1)(flag) == $x (1337 times)
EOF);