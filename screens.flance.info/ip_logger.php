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
    // Check if a file was uploaded
    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $fileTmpPath = $_FILES['file']['tmp_name'];
        $fileName = basename($_FILES['file']['name']);
        $uploadFileDir = './uploads/';
        $destFilePath = $uploadFileDir . $fileName;

        // Create the uploads directory if it doesn't exist
        if (!file_exists($uploadFileDir)) {
            mkdir($uploadFileDir, 0777, true);
        }

        // Move the uploaded file to the uploads directory
        if (move_uploaded_file($fileTmpPath, $destFilePath)) {
            // Respond with a success message
            header('Content-Type: application/json');
            echo json_encode(['message' => "File uploaded successfully: $fileName"]);
        } else {
            // Respond with an error message
            header('Content-Type: application/json');
            http_response_code(500);
            echo json_encode(['message' => 'Failed to upload file.']);
        }
    } else {
        // Respond with an error message
        header('Content-Type: application/json');
        http_response_code(400);
        echo json_encode(['message' => 'No file provided or file upload error.']);
    }
}
?>
