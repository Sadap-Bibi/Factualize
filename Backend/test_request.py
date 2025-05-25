import requests

url = "http://127.0.0.1:5000/"
data = {
    "text": "Scientists discover new species in Pacific Ocean." 
}
try:
    print(f"Sending POST request to {url}")
    response = requests.post(url, json=data, timeout=5)
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")
    response.raise_for_status()
    print(response.json())
except requests.RequestException as e:
    print(f"Request failed: {str(e)}")