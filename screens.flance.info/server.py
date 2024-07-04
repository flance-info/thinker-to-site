from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import json
import os
from datetime import datetime

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("Welcome to the IP Logger!")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Get the data
        parsed_data = urlparse.parse_qs(post_data)  # Parse the data

        local_ip = parsed_data.get('local_ip', [None])[0]  # Get the 'local_ip' value

        if local_ip:
            log = "Received IP: {0} at {1}\n".format(local_ip, datetime.now())
            with open('ip_log.txt', 'a') as log_file:
                log_file.write(log)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'IP address received: {0}'.format(local_ip)}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'No IP address provided.'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd server on port {0}...'.format(port))
    httpd.serve_forever()

if __name__ == "__main__":
    run()
