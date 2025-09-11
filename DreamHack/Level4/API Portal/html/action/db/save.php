<?php

$db_key = md5($param[0]);
$value_key = md5($param[0].$param[1]);
$value = base64_encode($param[2]);

@file_put_contents("/tmp/api-portal/db/$db_key/$value_key", $value);
echo "success";