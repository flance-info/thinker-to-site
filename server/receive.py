import socket
from PIL import Image
from io import BytesIO
from clipboard import send_to_clipboard  # Changed to absolute import
import win32clipboard
import threading
import time
import os
import keyboard  # Import the keyboard module

stop_server = False

def receive_screenshot():
    global stop_server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind to all available interfaces
    server_socket.listen(1)
    print("Server is running and waiting for connections...")
    if not os.path.exists('screens'):
       os.makedirs('screens')

    while not stop_server:
        server_socket.settimeout(1.0)
        try:
            client_socket, client_address = server_socket.accept()
        except socket.timeout:
            continue

        print(f"Connection from {client_address}")

        image_data = b''
        while True:
            packet = client_socket.recv(4096)
            if not packet:
                break
            image_data += packet

        client_socket.close()

        image = Image.open(BytesIO(image_data))

        # Save image locally with a unique filename
        timestamp = int(time.time())
        filename = f'received_screenshot_{timestamp}.png'
        filepath = os.path.join('screens', filename)
        image.save(filepath)
        print(f"Screenshot saved to {filepath}")

        # image.show()

        output = BytesIO()
        image.convert('RGB').save(output, format='BMP')
        data = output.getvalue()[14:]
        output.close()

        send_to_clipboard(win32clipboard.CF_DIB, data)
        print("Screenshot copied to clipboard!")

    server_socket.close()
    print("Server stopped.")

def stop_server_listener():
    global stop_server
    import keyboard
    keyboard.wait('esc')
    stop_server = True
    print("Server stopping...")

def start_server():
    listener_thread = threading.Thread(target=stop_server_listener)
    listener_thread.start()
    receive_screenshot()
