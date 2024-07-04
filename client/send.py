from io import BytesIO
import os
import requests


def send_local_ip_to_server(files):

    # URL of the server endpoint
   ## url = os.environ.get('SERVER_URL', 'http://screens.flance.info/ip_logger.php')
    url = os.environ.get('SERVER_URL', 'http://thinker-to-site.test/screens.flance.info/ip_logger.php')

    try:
        print("Sending screenshot to server...")
        response = requests.post(url, files=files)
        print(response.json())
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server. Make sure the server is running.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
