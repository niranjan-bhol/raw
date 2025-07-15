# IOC Order Margin Blocking Check 1

import asyncio
import aiohttp
import pyotp
import yarl  # For URL handling

# Credentials (Move to environment variables in production)
KITE_USERNAME = "DXU151"
KITE_PASSWORD = "Pratibha"
TOTP_KEY = "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP"

BASE_URL = "https://kite.zerodha.com/api"
ORDER_URL = "https://kite.zerodha.com/oms/orders/regular"

async def login(session):
    """Logs in to Zerodha and returns the authentication token."""
    try:
        async with session.post(
            f"{BASE_URL}/login",
            data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"}
        ) as res1:
            res1.raise_for_status()
            login_data = await res1.json()

        request_id = login_data.get("data", {}).get("request_id")
        user_id = login_data.get("data", {}).get("user_id")
        if not request_id or not user_id:
            print("Login failed: Missing request_id or user_id")
            return None

        # Perform two-factor authentication (TOTP)
        async with session.post(
            f"{BASE_URL}/twofa",
            data={
                "request_id": request_id,
                "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
                "user_id": user_id,
                "twofa_type": "totp"
            }
        ) as twofa_res:
            twofa_res.raise_for_status()
            print("Login successful")

        # Extract authentication token
        cookies = session.cookie_jar.filter_cookies(yarl.URL(BASE_URL))  # Fixed Deprecation Warning
        enctoken = cookies.get("enctoken")
        if not enctoken:
            print("Failed to retrieve authentication token.")
            return None

        return enctoken.value

    except aiohttp.ClientError as e:
        print(f"Login failed: {e}")
        return None


async def place_order(enctoken, session):
    """Places an order on Zerodha repeatedly with a 1-millisecond interval."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"enctoken {enctoken}"
    }

    order_data = {
        "variety": "regular",
        "exchange": "NSE",
        "tradingsymbol": "LIQUIDBEES",
        "transaction_type": "BUY",
        "order_type": "LIMIT",
        "quantity": 500,
        "price": 950,
        "product": "MIS",
        "validity": "IOC",
        "disclosed_quantity": 0,
        "trigger_price": 0,
        "squareoff": 0,
        "stoploss": 0,
        "trailing_stoploss": 0,
        "user_id": KITE_USERNAME
    }

    for i in range(10):  # Place order 10 times (modify as needed)
        try:
            async with session.post(ORDER_URL, headers=headers, data=order_data) as response:
                response.raise_for_status()
                order_response = await response.json()
                print(f"Order {i+1} placed: {order_response}")
        except aiohttp.ClientError as e:
            print(f"Order placement failed: {e}")
        
        await asyncio.sleep(0.001)  # Wait 1 millisecond before placing the next order | Remove await asyncio.sleep(0.001) → No waiting, just rapid execution.


async def main():
    """Main async function to handle login and order placement."""
    async with aiohttp.ClientSession() as session:
        enctoken = await login(session)
        if enctoken:
            await place_order(enctoken, session)

# Run the async event loop
if __name__ == "__main__":
    asyncio.run(main())
