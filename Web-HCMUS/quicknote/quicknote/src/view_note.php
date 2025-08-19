<?php
require_once 'classes.php';

$note_file = $_GET['file'] ?? '';
$note_file = basename($note_file);
$file_path = "notes/" . $note_file;

if (!empty($note_file) && file_exists($file_path) && pathinfo($file_path, PATHINFO_EXTENSION) === 'txt') {
    $serialized_note = file_get_contents($file_path);
    $note = unserialize($serialized_note);
    
    if ($note instanceof Note) {
        $note_time = strtotime($note->getTimestamp());
        $current_time = time();
        $one_day = 24 * 60 * 60; // 1 day in seconds
        
        if (($current_time - $note_time) > $one_day) {
            unlink($file_path);
            $page_title = "QuickNote";
            $navbar_title = "QuickNote - Note Expired";
            $content_template = 'template/view-note-error.php';
        } else {
            $content = $note->getNote();
            $note_info = $note;
            $page_title = "QuickNote";
            $navbar_title = "QuickNote - View Note";
            $content_template = 'template/view-note-content.php';
        }
    } else {
        $page_title = "QuickNote";
        $navbar_title = "QuickNote - Note Not Found";
        $content_template = 'template/view-note-error.php';
    }
} else {
    $page_title = "QuickNote";
    $navbar_title = "QuickNote - Note Not Found";
    $content_template = 'template/view-note-error.php';
}

include 'template/view-note.php';
?>