<?php
die();
// Disabled for a while due to the security reason (Command Injection)
// CREDIT: Vulnerability was reported by Kim.
$target = $param[0];

$cmd = "ping {$target}";
echo shell_exec($cmd);