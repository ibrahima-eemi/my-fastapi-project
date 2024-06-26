import requests

url = "http://127.0.0.1:8000/token"
data = {
    "username": "johndoe",
    "password": "secret"
}

response = requests.post(url, data=data)

if response.status_code == 200:
    token = response.json().get("access_token")
    print("Token:", token)
else:
    print("Failed to get token:", response.status_code, response.text)
