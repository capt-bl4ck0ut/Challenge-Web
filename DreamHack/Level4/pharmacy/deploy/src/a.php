<?php
$url = "http://localhost/index.php"; // URL server
$filePath = "deser.phar";            // File vừa tạo

$postFields = [
    "fileToUpload" => new CURLFile($filePath, "image/gif", "deser.gif"),
    "submit" => "upload"
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);

if(curl_errno($ch)) {
    echo "Error: " . curl_error($ch);
} else {
    echo "Server response:\n";
    echo $response;
}

curl_close($ch);
