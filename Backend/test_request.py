import requests

url = "http://127.0.0.1:5000/detect"
data = {
    "text": "The quick brown fox jumps over the lazy dog. Scientists discovered a new species in the Pacific Ocean."
}
response = requests.post(url, json=data)
print(response.json())