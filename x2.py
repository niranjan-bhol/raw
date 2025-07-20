import hashlib
import requests
import json

api_key = "lysrkggv6hknrry3"
api_secret = "fa95mv0re9vv36pzeu97km2qizq7zgl8"
request_token = "N4xZ0ObeBDnCQSFIjknHulxVl2gQML1M"

checksum_str = api_key + request_token + api_secret
checksum = hashlib.sha256(checksum_str.encode()).hexdigest()

res = requests.post(
    "https://api.kite.trade/session/token",
    headers={"X-Kite-Version": "3"},
    data={
        "api_key": api_key,
        "request_token": request_token,
        "checksum": checksum
    }
)

data = res.json()
access_token = data["data"]["access_token"]

# Save token to file for future use
with open("access_token.json", "w") as f:
    json.dump({"access_token": access_token}, f)

print("Access Token saved.")
