<?php
$id = $_GET["id"];

$mysqli = new mysqli('localhost','user','password','colorfulmemo');
if($mysqli){
    $stmt = $mysqli->prepare('SELECT title, color, content, adminCheck FROM memo WHERE id = ?');
    $stmt->bind_param('i',$id);
    $stmt->execute();
    $result = $stmt->get_result();
    $stmt->close();
}
else{
    die('db error');
}
$mysqli->close();

$row = mysqli_fetch_row($result);
if($row){
    $title = $row[0];
    $color = $row[1];
    $color = str_replace("<", "&lt;", $color);
    $color = str_replace(">", "&gt;", $color);
    $content = $row[2];
    $adminCheck = $row[3];
}
else{
    die('no such memo');
}

?>

<h2>Read Memo</h2>
<hr/>

<style>
    .content{
        color:<?php echo $color ?>
    }
</style>

<table class="table">
    <thead>
        <tr>
            <th scope="col" width="100px"></th>
            <th scope="col"></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Title</th>
            <td><?php echo htmlspecialchars($title); ?></td>
        </tr>
        <tr>
            <th scope="row">Checked</th>
            <td><?php echo $adminCheck==0?"X":"O"; ?></td>
        </tr>
        <tr>
            <th scope="row"></th>
            <td><a href=<?php echo '"/submit.php?id='.$id.'"' ?>>Submit memo to admin</a></td>
        </tr>
        <tr>
            <th scope="row" height="300px">Content</th>
            <td><span class="content"><?php echo htmlspecialchars($content); ?></span></td>
        </tr>
    </tbody>
</table>