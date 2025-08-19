<?php
error_reporting(0);
session_start();
require('vietlott.php');

if (!isset($_SESSION['secret'])) {
  $_SESSION['secret'] = random_bytes(4);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $numbers = $_POST["num"];
  $owner = $_POST["owner"];
  if (!is_array($numbers) || !is_string($owner)) {
    die("No hack!");
  }
  $numbers = array_map('intval', $numbers);
  foreach ($numbers as $num) {
    if ($num < 0 || $num > 45) {
      die("What?");
    }
  }
  $ticket = new VietlottTicket();
  $ticket->choices = $numbers;
  $ticket->owner = $owner;
  if (isset($_SESSION['secret'])) {
    $ticket->checksum = crc32(strval(crc32($_SESSION['secret'] . serialize($ticket))));  // One more for good measure
  } else {
    die("What?");
  }
  $_SESSION['last_checksum'] = $ticket->checksum;
  $cookie_ticket = base64_encode(serialize($ticket));
  setcookie('ticket', $cookie_ticket);
}

?>

<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="./static/style.css">
  <script src="./static/app.js" defer></script>
  <title>Vietlott</title>
</head>

<body>
  <h1 class="heading">Vietlott Mega 6/45</h1>
  <?php
  if (isset($_COOKIE['ticket']) || isset($cookie_ticket)) {
    $cookie_ticket = $cookie_ticket ?? $_COOKIE['ticket'];

    if (!($d = base64_decode($cookie_ticket))) die("Invalid ticket!");

    if (!($ticket = unserialize($d))) die("Invalid ticket!");

    if (!($ticket instanceof VietlottTicket)) die("Invalid ticket!");

    if (isset($_SESSION['secret']) && isset($_SESSION['last_checksum'])) {
      $win = $ticket->verify($_SESSION['secret'], $_SESSION['last_checksum']);
    } else {
      $win = false;
    }
  ?>
    <form method="POST" class="inp-form">
      <label class="input">
        <input class="input__field" type="text" name="owner" placeholder=" " autocomplete="off" value="<?php echo $ticket->owner; ?>" />
        <span class="input__label">Enter your name</span>
      </label>
      <div class="container">
        <?php foreach ($ticket->choices as $k => $number) { ?>
          <input type="text" class="num <?php echo $number === $ticket->result[$k] ? "correct" : "incorrect"; ?>" name="num[]" maxlength="2" required autocomplete="off" value="<?php echo $number; ?>">
        <?php } ?>
      </div>
    </form>
    <button class="button-19" style="max-width: fit-content;" role="button">Check!</button>
    <?php
    if ($win) {
      echo "Congratulation! You hit the jackpot, here is your flag:<br>";
      $fp = fopen("/flag.txt", "r");
      echo fgets($fp) . "<br>";
      fclose($fp);
    }
  } else {
    ?>
    <form method="POST" class="inp-form">
      <label class="input">
        <input class="input__field" type="text" name="owner" placeholder=" " autocomplete="off" />
        <span class="input__label">Enter your name</span>
      </label>
      <div class="container">
        <input type="text" class="num" name="num[]" maxlength="2" required autocomplete="off">
        <input type="text" class="num" name="num[]" maxlength="2" required autocomplete="off">
        <input type="text" class="num" name="num[]" maxlength="2" required autocomplete="off">
        <input type="text" class="num" name="num[]" maxlength="2" required autocomplete="off">
        <input type="text" class="num" name="num[]" maxlength="2" required autocomplete="off">
        <input type="text" class="num" name="num[]" maxlength="2" required autocomplete="off">
      </div>
    </form>
    <button class="button-19" style="max-width: fit-content;" role="button">Check!</button>
  <?php } ?>
</body>

</html>