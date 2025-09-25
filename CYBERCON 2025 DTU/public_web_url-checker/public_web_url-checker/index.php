<?php
if (!isset($_GET['u'])) {
    echo '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="/space.css">
<div class="container">
  <h1><span class="logo-dot"></span>Communication Checker</h1>
  <form method="get">
    <label>Toward the planet where I wish to send my message.</label>
    <input type="text" name="u" placeholder="http://example.com" style="width:100%">
    <button type="submit">Go</button>
  </form>
  <div class="footer">We can only determine whether the communication was received.</div>
</div>';
exit;
}

$url = $_GET['u'];
$raw = $_GET['b'] ?? '';

if (!isset($_SERVER['HTTP_USER_AGENT']) || stripos($_SERVER['HTTP_USER_AGENT'], '42') === false) {
    echo 'Do you know about the secret number?';
    exit;
}

if (!preg_match('#^https?://#i', $url)) {
    echo 'There is no such planet :(';
    exit;
}

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_TIMEOUT        => 30,
    CURLOPT_POSTFIELDS     => $raw,
]);

curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

$cls = ($http_code >= 200 && $http_code < 300) ? 'ok'
     : ($http_code >= 400 ? 'fail' : 'warn');
echo '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="/space.css">
<div class="container"><h1><span class="logo-dot"></span>URL Checker</h1>
<div class="status ' . $cls . '">Done (Status Code ' . $http_code . ')</div></div>';
