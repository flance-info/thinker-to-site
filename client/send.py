from io import BytesIO
import os
import requests


def send_local_ip_to_server(image_data):

    # URL of the server endpoint
   ## url = os.environ.get('SERVER_URL', 'http://screens.flance.info/ip_logger.php')
    url = os.environ.get('SERVER_URL', 'http://thinker-to-site.test/screens.flance.info/ip_logger.php')

    try:
        files = {'image': ('image.jpg', BytesIO(image_data), 'image/jpeg')}        
        headers = {'Content-Type': 'multipart/form-data'}
       # print(files)

        # Make the POST request
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the HTTP request
        print(f"Error occurred while sending local IP: {e}")
        return None, None
