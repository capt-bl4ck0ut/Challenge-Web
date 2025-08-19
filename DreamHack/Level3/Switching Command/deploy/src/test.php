<?php

include ("./config.php");

$pattern = '/\b(flag|nc|netcat|bin|bash|rm|sh)\b/i';

if($_SESSION["auth"] === "admin"){

    $command = isset($_GET["cmd"]) ? $_GET["cmd"] : "ls";
    $sanitized_command = str_replace("\n","",$command);
    if (preg_match($pattern, $sanitized_command)){
        exit("No hack");
    }
    $resulttt = shell_exec(escapeshellcmd($sanitized_command));
}
else if($_SESSION["auth"]=== "guest") {
    $command = "echo hi guest";
    $result = shell_exec($command);
}

else {
    $result = "Authentication first";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Command Test</title>
</head>
<body>
    <h2>Command Test</h2>
    <?php
    echo "<pre>$result</pre>";
    ?>
</body>
</html>