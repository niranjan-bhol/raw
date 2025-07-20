import requests
import hashlib

# Replace these with your actual values
api_key = "lysrkggv6hknrry3"
api_secret = "fa95mv0re9vv36pzeu97km2qizq7zgl8"
request_token = "Yrmn86nF1IZr2U3EFN5ieG6v24s9nkSm"

# Create SHA256 checksum
checksum_input = api_key + request_token + api_secret
checksum = hashlib.sha256(checksum_input.encode()).hexdigest()

# Make the request
url = "https://api.kite.trade/session/token"
headers = {"X-Kite-Version": "3"}
data = {
    "api_key": api_key,
    "request_token": request_token,
    "checksum": checksum
}

response = requests.post(url, headers=headers, data=data)

# Parse and print result
if response.status_code == 200:
    access_token = response.json()
    print("✅ Access Token:", access_token)
else:
    print("❌ Failed to get access token:")
    print("Status:", response.status_code)
    print("Response:", response.json())
