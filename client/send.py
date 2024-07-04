import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def send_local_ip_to_server(files):
    # URL of the server endpoint
    url = os.environ.get('SERVER_URL', 'https://screens.flance.info/ip_logger.php')

    # Set up a session with retry logic
    session = requests.Session()
    retry = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # A delay factor between retries
        status_forcelist=[500, 502, 503, 504]  # Retry on these HTTP status codes
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        print("Sending screenshot to ser")
        response = session.post(url, files=files)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(url, response.json())
    except requests.exceptions.ConnectionError:
        print(url, "Failed to connect to the server. Make sure the server is running.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage (make sure to define `files` correctly in the surrounding code)
# buffer = BytesIO()
# screenshot.save(buffer, format='PNG')
# buffer.seek(0)
# files = {'file': ('screenshot.png', buffer, 'image/png')}
# send_local_ip_to_server(files)
