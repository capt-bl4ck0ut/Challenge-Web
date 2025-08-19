<?php
    ini_set("session.upload_progress.enabled", "Off");
    ini_set("file_uploads", "Off");
    ini_set('display_errors', '0');

    if(isset($_GET["file"])) {
        if (preg_match("/^(file:|http:|ftp:|zlib:|data:|glob:|phar:|zip:|expect:|php:)/i", $_GET["file"])) {
            die("HAHA... 😀");
        }
        include($_GET["file"]);
    }
?>
