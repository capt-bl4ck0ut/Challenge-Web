<?php

@mkdir("/tmp/api-portal/db");

$real_key = md5($param[0]);
@mkdir("/tmp/api-portal/db/$real_key");
die("success");