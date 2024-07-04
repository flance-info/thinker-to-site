import socket
import time
from utils import get_local_ip

def broadcast_ip():
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.settimeout(0.2)

    local_ip = get_local_ip()
    message = f'SERVER_IP:{local_ip}'.encode('utf-8')

    while True:
        broadcast_socket.sendto(message, ('<broadcast>', 12345))
        time.sleep(5)
