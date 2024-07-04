import requests
from utils import get_local_ip
# URL of the PHP script
url = 'http://screens.flance.info/ip_logger.php'
local_ip = get_local_ip()
# Data to be sent in the POST request
data = {
    'local_ip': local_ip
}

# Make the POST request
response = requests.post(url, data=data)

# Print the response
print('Response Code:', response.status_code)
print('Response Body:', response.text)
