import time

start_time = time.time()

result = 0
for i in range(1000000):
    result += i * i  # Simple computation

end_time = time.time()
print(f"Execution Time: {end_time - start_time:.6f} seconds")

# python3 measure_time.py
