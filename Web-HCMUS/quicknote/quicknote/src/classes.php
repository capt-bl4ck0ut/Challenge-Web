<?php

class User
{
    public $username;
    public $premium_key;

    public function __construct($username, $premium_key = null)
    {
        $this->username = $username;
        $this->premium_key = $premium_key;
    }

    public function isPremium()
    {
        return $this->premium_key == $_ENV['PREMIUM_KEY'];
    }
}

class Note
{
    private $ip;
    private $name;
    private $note;
    private $timestamp;

    public function __construct($ip, $name, $note)
    {
        $this->ip = $ip;
        $this->name = $name;
        $this->note = $note;
        $this->timestamp = date('Y-m-d H:i:s');
    }

    public function getNote()
    {
        return $this->note;
    }

    public function getTimestamp()
    {
        return $this->timestamp;
    }

    public function validateNote($is_premium = false)
    {
        if ($is_premium) {
            return $this->note;
        } else {
            $note_regex = '/^[\w\s.,!?-]{1,500}$/';
            return preg_match($note_regex, $this->note);
        }
    }

    public function __destruct()
    {
        $log_entry = "[{$this->timestamp}] IP: {$this->ip} | User: {$this->name} | Note: " . substr($this->note, 0, 100);
        system("echo '$log_entry' >> /quicknote/access.log");
    }
}
?>