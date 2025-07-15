orders = [
    {
        "variety": "regular",
        "exchange": "NSE",
        "tradingsymbol": "LIQUIDBEES",
        "transaction_type": "BUY",
        "order_type": "LIMIT",
        "quantity": 1,
        "price": 1000,
        "product": "MIS",
        "validity": "DAY",
    },
    {
        "variety": "regular",
        "exchange": "NSE",
        "tradingsymbol": "LIQUIDBEES",
        "transaction_type": "SELL",
        "order_type": "LIMIT",
        "quantity": 1,
        "price": 1000,
        "product": "MIS",
        "validity": "DAY",
    }
]


import pyotp
import aiohttp
import asyncio
from datetime import datetime

# Zerodha credentials
KITE_USERNAME = 'DXU151'
KITE_PASSWORD = 'Pratibha'
TOTP_KEY = 'FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP'

enctoken = None

# Function 1: Login to Zerodha
async def login():
    """
    Handles the login process to Zerodha using credentials.
    Updates the global enctoken variable.
    """
    global enctoken
    try:
        async with aiohttp.ClientSession() as session:
            # Step 1: Login request
            res1 = await session.post(
                'https://kite.zerodha.com/api/login',
                data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"}
            )
            login_res = await res1.json()

            if login_res.get('status') != 'success':
                raise Exception("Login failed: " + login_res.get('message', 'Unknown error'))

            # Step 2: Two-factor authentication
            final_res = await session.post(
                'https://kite.zerodha.com/api/twofa',
                data={
                    "request_id": login_res['data']['request_id'],
                    "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
                    "user_id": login_res['data']['user_id'],
                    "twofa_type": "totp"
                }
            )
            final_res_json = await final_res.json()

            if final_res_json.get('status') != 'success':
                raise Exception("Two-factor authentication failed: " + final_res_json.get('message', 'Unknown error'))

            # Extract cookies
            cookies = session.cookie_jar.filter_cookies('https://kite.zerodha.com')
            enctoken = cookies.get('enctoken').value if 'enctoken' in cookies else None

            if not enctoken:
                raise Exception("Failed to retrieve enctoken.")

            print(f"Login successful at {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error during login: {e}")

# Function 2: Execute a Single Order
async def execute_order(session, order_data):
    """
    Executes a single order on the Zerodha platform.
    """
    try:
        url = 'https://kite.zerodha.com/oms/orders/regular'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "https://kite.zerodha.com/dashboard",
            "Accept-Language": "en-US,en;q=0.6",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            'Authorization': f"enctoken {enctoken}"
        }

        async with session.post(url, headers=headers, data=order_data) as response:
            response_data = await response.json()

            if response.status == 200 and response_data.get('status') == 'success':
                dt = datetime.now()
                print(f"{dt} - Order placed successfully for {order_data['tradingsymbol']}: {response_data}")
            else:
                print(f"{dt} - Order placement failed for {order_data['tradingsymbol']}: " + response_data.get('message', 'Unknown error'))
    except Exception as e:
        print(f"Error during order execution: {e}")

# Function 3: Execute All Orders
async def execute_all_orders():
    """
    Executes all orders concurrently.
    """
    if not enctoken:
        print("Error: Login has not been performed yet.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [execute_order(session, order) for order in orders]
        await asyncio.gather(*tasks)

# Function 4: Main Execution Logic
async def main():
    # Set the target time for login (9:14:00 AM)
    target_time_login = datetime.now().replace(hour=9, minute=14, second=0, microsecond=0)

    # Set the target time for order execution (9:15:00 AM)
    target_time_orders = datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)

    # Wait until the login target time
    await asyncio.sleep((target_time_login - datetime.now()).total_seconds())

    # Perform login
    await login()

    # Wait until the order execution target time
    await asyncio.sleep((target_time_orders - datetime.now()).total_seconds())

    # Execute all orders
    await execute_all_orders()

if __name__ == "__main__":
    asyncio.run(main())
