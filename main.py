import tkinter as tk
import threading
import os
import subprocess
from PIL import Image, ImageDraw
import pystray
import sys
import logging
from logging import StreamHandler

client_process = None
server_process = None
icon = None

class TextHandler(StreamHandler):
    """This class allows logging to a Tkinter Text widget"""
    def __init__(self, text_widget):
        StreamHandler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

def run_client():
    global client_process
    logging.info("Starting client...")
    client_button.config(text="Client Processing...")
    client_process = subprocess.Popen(['python', 'client/client.py'])
    stop_client_button.config(state=tk.NORMAL)
    stop_all_button.config(state=tk.NORMAL)

def run_server():
    global server_process
    logging.info("Starting server...")
    server_button.config(text="Server Processing...")
    server_process = subprocess.Popen(['python', 'server/main.py'])
    stop_server_button.config(state=tk.NORMAL)
    stop_all_button.config(state=tk.NORMAL)

def stop_client():
    global client_process
    if client_process:
        logging.info("Stopping client...")
        client_process.terminate()
        client_process = None
        client_button.config(text="Start Client")
        stop_client_button.config(state=tk.DISABLED)
        if server_process is None:
            stop_all_button.config(state=tk.DISABLED)

def stop_server():
    global server_process
    if server_process:
        logging.info("Stopping server...")
        server_process.terminate()
        server_process = None
        server_button.config(text="Start Server")
        stop_server_button.config(state=tk.DISABLED)
        if client_process is None:
            stop_all_button.config(state=tk.DISABLED)

def stop_all():
    stop_client()
    stop_server()

def create_image():
    # Generate an image and draw a pattern
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=(255, 0, 0))
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=(0, 255, 0))
    dc.rectangle(
        (width // 2, height // 2, width, height),
        fill=(0, 0, 255))
    dc.rectangle(
        (0, 0, width // 2, height // 2),
        fill=(255, 255, 0))

    return image

def on_closing():
    hide_window()

def hide_window():
    global icon
    app.withdraw()
    if icon is None:
        icon = pystray.Icon("Thinker")
        icon.icon = create_image()
        icon.title = "Thinker"
        icon.menu = pystray.Menu(
            pystray.MenuItem("Open", lambda: show_window()),
            pystray.MenuItem("Quit", lambda: quit_app())
        )
        threading.Thread(target=icon.run, daemon=True).start()

def show_window():
    global icon
    app.after(0, app.deiconify)
    if icon:
        icon.stop()
        icon = None

def quit_app():
    global icon
    stop_all()
    if icon:
        icon.stop()
        icon = None
    app.quit()

app = tk.Tk()
app.title("Thinker")
app.geometry("600x400")

# Override the close button
app.protocol("WM_DELETE_WINDOW", on_closing)

# Frame for client buttons
client_frame = tk.Frame(app)
client_frame.pack(pady=10)

client_button = tk.Button(client_frame, text="Start Client", command=run_client)
client_button.grid(row=0, column=0, padx=5)

stop_client_button = tk.Button(client_frame, text="Stop Client", command=stop_client, state=tk.DISABLED)
stop_client_button.grid(row=0, column=1, padx=5)

# Frame for server buttons
server_frame = tk.Frame(app)
server_frame.pack(pady=10)

server_button = tk.Button(server_frame, text="Start Server", command=run_server)
server_button.grid(row=0, column=0, padx=5)

stop_server_button = tk.Button(server_frame, text="Stop Server", command=stop_server, state=tk.DISABLED)
stop_server_button.grid(row=0, column=1, padx=5)

stop_all_button = tk.Button(app, text="Stop All", command=stop_all, state=tk.DISABLED)
stop_all_button.pack(pady=10)

# Text widget for logging
log_frame = tk.Frame(app)
log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
log_text = tk.Text(log_frame, wrap='word')
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
log_scroll = tk.Scrollbar(log_frame, command=log_text.yview)
log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=log_scroll.set)

# Set up logging
text_handler = TextHandler(log_text)
logging.basicConfig(level=logging.INFO, handlers=[text_handler])

app.mainloop()
