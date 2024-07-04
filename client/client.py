import socket
import win32clipboard
from PIL import ImageGrab, Image
from io import BytesIO
import keyboard
import time
import struct

def discover_server_ip():
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discovery_socket.bind(('', 12345))

    while True:
        data, addr = discovery_socket.recvfrom(1024)
        message = data.decode('utf-8')
        if message.startswith('SERVER_IP:'):
            server_ip = message.split(':')[1]
            print(f"Discovered server IP: {server_ip}")
            return server_ip

def get_clipboard_image():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
        win32clipboard.CloseClipboard()

        image = ImageGrab.grabclipboard()
        if image is None:
            print("No image found in clipboard.")
            return
    except TypeError:
        image = None

    return image

def send_screenshot(server_ip):
   # Give some time for the screenshot to be copied to the clipboard
    time.sleep(1)
    screenshot = get_clipboard_image()
    if screenshot is None:
        print("No image found in clipboard.")
        return

    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    buffer.close()

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 12345))
        client_socket.sendall(image_data)
        client_socket.close()
        print("Screenshot sent!")
    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running.")

if __name__ == "__main__":
    print("Discovering server...")
    ##server_ip = discover_server_ip()
    server_ip = "192.168.1.236"
    print("Press Alt + Print Screen to send a screenshot from clipboard")
    keyboard.add_hotkey('alt+print_screen', lambda: send_screenshot(server_ip))

    # Keep the script running
    keyboard.wait('esc')  # Press 'Esc' to stop the script
