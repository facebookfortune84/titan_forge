import urllib.request
import time
import sys

print(sys.path)

time.sleep(5) # Wait for 5 seconds

try:
    with urllib.request.urlopen("http://localhost:8000/api/v1/landing_page_html") as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
