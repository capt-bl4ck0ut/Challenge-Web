<?php
//TODO: Change to php-curl

$url = "http://".$param[0]; //TODO: support ssl context
$ip = $param[1];
$referer = $param[2];

$header = "User-Agent: API Portal Proxy\r\n";
$header .= "X-Forwarded-For: {$ip}\r\n";
$header .= "X-Api-Referer: {$referer}";

$ctx = stream_context_create(array(
    'http' => array(
        'method' => 'POST',
        "content" => "", //TODO: implement
        'header' => $header
    )
));

die(file_get_contents($url, null, $ctx));