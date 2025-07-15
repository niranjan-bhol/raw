import time
import asyncio
import requests
import aiohttp
import httpx
from concurrent.futures import ThreadPoolExecutor

URL = "https://zerodha.com/"
NUM_REQUESTS = 10


# 1️⃣ Synchronous Requests
def sync_requests():
    start = time.time()
    for _ in range(NUM_REQUESTS):
        requests.get(URL)
    print(f"Requests (Synchronous) : {time.time() - start:.4f} seconds")


# 2️⃣ ThreadPoolExecutor (Multithreading)
def fetch_request(_):
    return requests.get(URL)


def threadpool_requests():
    start = time.time()
    with ThreadPoolExecutor() as executor:
        list(executor.map(fetch_request, range(NUM_REQUESTS)))
    print(f"ThreadPoolExecutor (Asynchronous) : {time.time() - start:.4f} seconds")


# 3️⃣ Aiohttp (Async)
async def fetch_aiohttp(session):
    async with session.get(URL) as response:
        return await response.text()


async def aiohttp_requests():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_aiohttp(session) for _ in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)
    print(f"Aiohttp (Asynchronous) : {time.time() - start:.4f} seconds")


# 4️⃣ Httpx (Async)
async def fetch_httpx(client):
    response = await client.get(URL)
    return response.text


async def httpx_requests():
    start = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_httpx(client) for _ in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)
    print(f"Httpx (Asynchronous) : {time.time() - start:.4f} seconds")


# 🚀 Run benchmarks
if __name__ == "__main__":
    print(f"Testing {NUM_REQUESTS} requests using requests, aiohttp, httpx, ThreadPoolExecutor\n")
    
    sync_requests()
    asyncio.run(aiohttp_requests())
    asyncio.run(httpx_requests())
    threadpool_requests()

"""
pip3 install requests aiohttp httpx

python3 async_requests_comparison.py
"""
