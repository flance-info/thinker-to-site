<?php
// Log file path
$logFile = 'ip_log.txt';

// Get the client's IP address
$clientIP = $_SERVER['REMOTE_ADDR'];

// Handle GET request
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo "Welcome to the IP Logger!";
}

// Handle POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Check if 'local_ip' is provided in the POST data
    if (isset($_POST['local_ip'])) {
        $localIP = $_POST['local_ip'];
        $logEntry = "Received IP: $localIP at " . date('Y-m-d H:i:s') . "\n";

        // Append the log entry to the log file
        file_put_contents($logFile, $logEntry, FILE_APPEND);

        // Respond with a success message
        header('Content-Type: application/json');
        echo json_encode(['message' => "IP address received: $localIP"]);
    } else {
        // Respond with an error message
        header('Content-Type: application/json');
        http_response_code(400);
        echo json_encode(['message' => 'No IP address provided.']);
    }
}
?>
