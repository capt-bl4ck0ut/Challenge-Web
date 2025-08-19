<?php
class VietlottTicket {
  public $owner;
  public $result;
  public $choices;
  public $checksum;

  function verify($secret, $last_checksum) {
    if (!is_array($this->choices)) return false;
    if (count($this->choices) !== 6) return false;

    $ticket_checksum = $this->checksum;
    $this->checksum = null;
    $this->checksum = crc32(strval(crc32($secret . serialize($this))));
    if ($ticket_checksum !== $this->checksum || $last_checksum !== $this->checksum) {
      echo "Ticket's checksum is wrong: " . $this->checksum . "<br>";
      return false;
    }

    if (!ctype_print($this->owner)) {
      echo "Weird name, suspicious hmmm<br>";
      return false; 
    }

    $true_result = roll(6);
    for ($i = 0; $i < 6; $i++) {
      $this->result[$i] = $true_result[$i];
    }

    for ($i = 0; $i < 6; $i++) {
      if ($this->result[$i] !== $this->choices[$i]) {
        return false;
      }
    }

    return true;
  }
}

function roll($n) {
  $res = array();
  for ($i = 0; $i < $n; $i++) {
    $res[$i] = random_int(0, 100000) % 46;
  } 
  return $res;
}

?>