<?php
	$conn = mysqli_connect("db", "dreamhack", "dreamhack", "dreamhack");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
?>