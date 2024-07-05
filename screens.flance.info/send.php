<?php
$server_ip = '84.54.92.46'; // Replace with your PC's IP address
$server_port = 8000;        // Replace with the port your PC server is listening on
$file_path = '/upload/screenshot.png'; // Path to the file you want to send

// Open a socket connection to the server
$socket = fsockopen($server_ip, $server_port, $errno, $errstr, 30);

if (!$socket) {
    echo "Error: $errno - $errstr\n";
} else {
    // Open the file
    $file = fopen($file_path, 'rb');
    if ($file) {
        // Send the file data
        while (!feof($file)) {
            $data = fread($file, 8192); // Read file in chunks
            fwrite($socket, $data);
        }
        fclose($file);
    } else {
        echo "Failed to open file: $file_path\n";
    }

    // Close the socket connection
    fclose($socket);
    echo "File sent successfully.\n";
}
?>
