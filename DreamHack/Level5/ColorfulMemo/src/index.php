<?php
    $path = $_GET["path"];
    if($path == ""){
        $path = "main";
    }
    $path = "./".$path.".php";
?>

<style>
.body {
    padding-top:5%;
    padding-left:5%;
    padding-right:5%;
}
</style>

<!DOCTYPE html>
<html>
    <head>
        <?php include_once "./include.php"; ?>
    </head>
    <body>
        <?php include_once "./header.php"; ?>
        <div class="body">
            <?php include_once $path; ?>
        </div>
    </body>
</html>