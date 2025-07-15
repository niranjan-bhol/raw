import requests
import time

URL = "https://www.example.com"  # Change this to your target URL # https://www.zerodha.com
NUM_REQUESTS = 10  # Number of requests to send

start_time = time.time()

for _ in range(NUM_REQUESTS):
    response = requests.get(URL)
    
end_time = time.time()

total_time = end_time - start_time
average_time = total_time / NUM_REQUESTS

print(f"Sent {NUM_REQUESTS} requests in {total_time:.6f} seconds")
print(f"Average time per request: {average_time:.6f} seconds")

# python3 request_speed_test.py
