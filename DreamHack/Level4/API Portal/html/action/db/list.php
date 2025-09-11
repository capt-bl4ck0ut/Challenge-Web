<?php

$dbs = scandir("/tmp/api-portal/db");
$dbs = array_diff($dbs, array(".", ".."));

die(implode(";", $dbs));