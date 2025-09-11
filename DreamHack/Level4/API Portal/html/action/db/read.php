<?php

$db_key = md5($param[0]);
$value_key = md5($param[0].$param[1]);

$content = @file_get_contents("/tmp/api-portal/db/$db_key/$value_key");

header("Content-Type: text/plain");
die(base64_decode($content));

