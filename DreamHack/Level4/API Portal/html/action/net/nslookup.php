<?php
die();
// Disabled for a while due to the security reason (Command Injection)
// CREDIT: Vulnerability was reported by Kim.
$domain = $param[0];
$record = $param[1];

$cmd = "nslookup -type={$record} $domain";
echo shell_exec($cmd);