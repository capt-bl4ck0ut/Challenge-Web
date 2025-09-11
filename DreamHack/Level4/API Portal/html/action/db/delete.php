<?php

$real_key = md5($param[0]);
@system("rm -rf /tmp/api-portal/db/$real_key");
die("success");