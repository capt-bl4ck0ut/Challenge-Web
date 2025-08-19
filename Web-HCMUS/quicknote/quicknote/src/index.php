<?php
require_once 'classes.php';

$current_user = new User('anonymous', '');

if (isset($_COOKIE['user'])) {
    try {
        $current_user = unserialize(strip_tags($_COOKIE['user']));
        if (!$current_user instanceof User) {
            throw new Exception("Invalid user object");
        }
    } catch (Exception $e) {
        $current_user = new User('anonymous', '');
    }
}

if ($_POST) {
    $action = $_POST['action'] ?? '';

    if ($action === 'login') {
        $username = $_POST['username'] ?? '';
        $premium_key = $_POST['premium_key'] ?? '';
        $user = new User($username, $premium_key);
        $serialized_user = serialize($user);
        setcookie('user', $serialized_user, time() + 3600, '/');
        header("Location: index.php");
        exit();
    }

    if ($action === 'add_note') {
        $note_content = $_POST['note'] ?? '';
        $user_ip = $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1';
        $note_content = str_replace("'", '"', subject: $note_content);
        $note = new Note($user_ip, $current_user->username, $note_content);

        if ($note->validateNote($current_user->isPremium())) {
            $random_hex = bin2hex(random_bytes(8));
            $filename = "notes/{$current_user->username}_{$random_hex}.txt";
            file_put_contents($filename, serialize($note));

            $note_filename = basename($filename);
            $message = "Note added successfully! <a href=\"view_note.php?file=$note_filename\" target=\"_blank\">View Note</a>";
        } else {
            $message = "Invalid note format or length!";
        }
    }
}
include 'template/main.php';
?>