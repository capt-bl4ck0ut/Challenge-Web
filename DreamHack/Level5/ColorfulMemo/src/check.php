<?php
if($_SERVER["REMOTE_ADDR"] == '127.0.0.1' || $_SERVER["REMOTE_ADDR"] == '::1'){
    $id = $_GET['id'];
    $mysqli = new mysqli('localhost','user','password','colorfulmemo');
    // I believe admin
    $result = $mysqli->query('SELECT adminCheck FROM memo WHERE id = '.$id);
    if($result){
        $row = mysqli_fetch_row($result);
        if($row){
            if($row[0] != 1){
                $stmt = $mysqli->prepare('UPDATE memo SET adminCheck = 1 WHERE id = ?');
                $stmt->bind_param('i',$id);
                $stmt->execute();
                $stmt->close();
            }
        }
    }
}
else{
    die("no hack");
}
?>