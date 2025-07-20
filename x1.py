import asyncio
import aiohttp
import json
from datetime import datetime

API_KEY = "lysrkggv6hknrry3"
KITE_API_URL = "https://api.kite.trade/orders/regular"

# Load access token from file
with open("access_token.json") as f:
    ACCESS_TOKEN = json.load(f)["access_token"]

HEADERS = {
    "X-Kite-Version": "3",
    "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Sample payload — modify per order needs
order_payload = {
    "exchange": "NSE",
    "tradingsymbol": "INFY",
    "transaction_type": "BUY",
    "order_type": "MARKET",
    "quantity": 1,
    "product": "MIS",
    "validity": "DAY"
}


async def place_order(session, order_id):
    async with session.post(KITE_API_URL, headers=HEADERS, data=order_payload) as resp:
        status = resp.status
        try:
            data = await resp.json()
        except:
            data = await resp.text()
        #print(f"Order {order_id}: Status {status}, Response: {data}")


async def main():
    async with aiohttp.ClientSession() as session:
        print(datetime.now())
        tasks = [place_order(session, i + 1) for i in range(10)]
        await asyncio.gather(*tasks)
        print(datetime.now())


if __name__ == "__main__":
    asyncio.run(main())
