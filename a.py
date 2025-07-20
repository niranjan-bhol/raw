import hashlib

api_key = "lysrkggv6hknrry3"
request_token = "SavvnyvQhS2CGS3cqMNUQjaVe8OLqn7N"
api_secret = "fa95mv0re9vv36pzeu97km2qizq7zgl8"

checksum_str = api_key + request_token + api_secret
checksum = hashlib.sha256(checksum_str.encode('utf-8')).hexdigest()

print(checksum)

