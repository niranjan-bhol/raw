import requests

# Define the API endpoint
url = "https://api.kite.trade/session/token"

# Define headers
headers = {
    "X-Kite-Version": "3"
}

# Define payload data
payload = {
    "api_key": "lysrkggv6hknrry3",
    "request_token": "SavvnyvQhS2CGS3cqMNUQjaVe8OLqn7N",
    "checksum": "b769b0a659c81a06d3f31322019f7eb0919fdb30a6452ee6c37b6c230e5e4142"
}

# Make the POST request
response = requests.post(url, headers=headers, data=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())

# Make the POST request
response = requests.post(url, headers=headers, data=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())