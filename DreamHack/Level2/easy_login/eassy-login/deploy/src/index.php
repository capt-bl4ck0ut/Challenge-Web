<?php

function generatePassword($length) {
    $characters = '0123456789abcdef';
    $charactersLength = strlen($characters);
    $pw = '';
    for ($i = 0; $i < $length; $i++) {
        $pw .= $characters[random_int(0, $charactersLength - 1)];
    }
    return $pw;
}

function generateOTP() {
    return 'P' . str_pad(strval(random_int(0, 999999)), 6, "0", STR_PAD_LEFT);
}

$admin_pw = generatePassword(32);
$otp = generateOTP();

function login() {
    if (!isset($_POST['cred'])) {
        echo "Please login...";
        return;
    }

    if (!($cred = base64_decode($_POST['cred']))) {
        echo "Cred error";
        return;
    }

    if (!($cred = json_decode($cred, true))) {
        echo "Cred error";
        return;
    }

    if (!(isset($cred['id']) && isset($cred['pw']) && isset($cred['otp']))) {
        echo "Cred error";
        return;
    }

    if ($cred['id'] != 'admin') {
        echo "Hello," . $cred['id'];
        return;
    }
    
    if ($cred['otp'] != $GLOBALS['otp']) {
        echo "OTP fail";
        return;
    }

    if (!strcmp($cred['pw'], $GLOBALS['admin_pw'])) {
        require_once('flag.php');
        echo "Hello, admin! get the flag: " . $flag;
        return;
    }

    echo "Password fail";
    return;
}

?>

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>Easy Login</title>
</head>
<body>
    <div class="login-container">
        <h2>Login as admin to get flag<h2>
        <form action="login.php" method="post">
            <div class="form-group">
                <label for="id">ID</label>
                <input type="text" name="id"></br>
            </div>
            <div class="form-group">
                <label for="pw">PW</label>
                <input type="text" name="pw"></br>
            </div>
            <div class="form-group">
                <label for="otp">OTP</label>
                <input type="text" name="otp"></br>
            </div>
            <button type="submit" class="button">Login</button>
        </form>
        <div class="message">
            <?php login(); ?>
        </div>
    </div>
</body>
</html>
