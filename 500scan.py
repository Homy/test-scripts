import requests
import urllib.parse

# Define the target website URL
target_url = "https://www.example.com"

# Send a GET request to the target URL and parse the response HTML
response = requests.get(target_url)
html_content = response.content.decode("utf-8")

# Parse the HTML to find all links to internal pages on the target website
internal_links = set()
for link in html_content.split("href="):
    if link.startswith('"') or link.startswith("'"):
        link = link[1:]
    if link.endswith('"') or link.endswith("'"):
        link = link[:-1]
    if link.startswith("/") or link.startswith(target_url):
        internal_links.add(link)
    elif link.startswith("http"):
        parsed_link = urllib.parse.urlparse(link)
        if parsed_link.netloc == urllib.parse.urlparse(target_url).netloc:
            internal_links.add(link)

# Send GET requests to all detected endpoints and print any 5xx responses
for endpoint in internal_links:
    try:
        response = requests.get(endpoint)
        if response.status_code >= 500:
            print(f"{endpoint} returned status code {response.status_code}")
    except requests.exceptions.RequestException:
        print(f"Error requesting {endpoint}")
