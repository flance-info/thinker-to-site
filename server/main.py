from broadcast import broadcast_ip
from receive import start_server
import threading

if __name__ == "__main__":
    threading.Thread(target=broadcast_ip, daemon=True).start()
    start_server()

