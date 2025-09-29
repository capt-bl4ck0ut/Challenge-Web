<?php
$id = $_GET['id'];
if(ctype_digit($id)){
    exec("python3 /bot.py ".$id);
}
else{
    die("no hack");
}
die('<script> location.href="/" </script>');
?>