<?php

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $filename = $_GET['filename'] ?? 'log.csv';
    $startTimestamp = isset($_GET['start']) ? intval($_GET['start']) : 0;
    $endTimestamp = isset($_GET['end']) ? intval($_GET['end']) : time();
    
    if (!file_exists($filename)) {
        echo "Database is not ready!";
        exit;
    }

    $returnData = [];
    $file = fopen($filename, "r");

    while (($line = fgetcsv($file)) !== FALSE) {
        [$timestamp, $downloadSpeed, $uploadSpeed] = $line;
        if ($timestamp >= $startTimestamp && $timestamp <= $endTimestamp) {
            $returnData[] = [
                'timestamp' => $timestamp,
                'downloadSpeed' => $downloadSpeed,
                'uploadSpeed' => $uploadSpeed
            ];
        }
    }

    fclose($file);

    if (empty($returnData)) {
        echo "Database is not ready!";
    } else {
        echo json_encode($returnData);
    }
}
?>