<?php
$mysqli = new mysqli('localhost','user','password','colorfulmemo');
if($mysqli){
    $result = $mysqli->query('SELECT id, title, adminCheck FROM memo');
}
else{
    die('db error');
}
$mysqli->close();

?>

<h2>List Memo</h2>
<hr/>

<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col" width="70%">title</th>
            <th scope="col">checked</th>
        </tr>
    </thead>
    <tbody>
        <?php while($row = mysqli_fetch_row($result)){ ?>
            <tr>
                <th scope="row"><?php echo $row[0]; ?></th>
                <td><a href=<?php echo '"/?path=read&id='.$row[0].'"'; ?>><?php echo htmlspecialchars($row[1]); ?></a></td>
                <td><?php echo $row[2]==0?"X":"O"; ?></td>
            </tr>
        <?php } ?>
    </tbody>
</table>