<?php
if($_SERVER['REQUEST_METHOD'] == 'POST'){
    $memoTitle = $_POST['memoTitle'];
    $memoColor = $_POST['memoColor'];
    $memoContent = $_POST['memoContent'];

    $mysqli = new mysqli('localhost','user','password','colorfulmemo');

    if($mysqli){
        $stmt = $mysqli->prepare('INSERT INTO memo (title, color, content, adminCheck) VALUES (?,?,?,0)');
        $stmt->bind_param('sss',$memoTitle,$memoColor,$memoContent);
        $stmt->execute();
        $stmt->close();
    }
    else{
        die('db error');
    }
    $mysqli->close();
    die('<script> location.href="/" </script>');
}
?>

<h2>Write Memo</h2>
<hr/>

<form method="post">
    <label for="memoTitle" class="form-label">Title</label>
    <input name="memoTitle" id="memoTitle" class="form-control" type="text">
    <br/>
    <label for="memoColor" class="form-label">Color</label>
    <select name="memoColor" id="memoColor" class="form-select">
        <option value="black">Black</option>
        <option value="red">Red</option>
        <option value="blue">Blue</option>
        <option value="green">Green</option>
        <option value="yellow">Yellow</option>
    </select>
    <label for="memoContent" class="form-label">Content</label>
    <textarea name="memoContent" class="form-control" id="memoContent" rows="5" style="resize:none;"></textarea>
    <br/>
    <button type="submit" class="btn btn-primary">Write</button>
</form>