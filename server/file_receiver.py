import socket

def receive_file():
    server_ip = '0.0.0.0'  # Listen on all network interfaces
    server_port = 5001      # Choose any port number that is open
    buffer_size = 4096      # Size of each data chunk received
    save_file_path = 'received_file.txt'  # Path to save the received file

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"Listening on {server_ip}:{server_port}")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    with open(save_file_path, 'wb') as file:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            file.write(data)
    conn.close()
    print("File received successfully.")

if __name__ == "__main__":
    receive_file()
