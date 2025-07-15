# Zerodha Batch Orders Support or Not 1

import pyotp
import requests

# Credentials
KITE_USERNAME = "DXU151"
KITE_PASSWORD = "Pratibha"
TOTP_KEY = "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP"

BASE_URL = "https://kite.zerodha.com/api"
session = requests.Session()

def login():
    """Logs in to Zerodha and returns the session with authentication."""
    res1 = session.post(f"{BASE_URL}/login", data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"})
    res1.raise_for_status()
    login_data = res1.json()

    # Perform two-factor authentication (TOTP)
    twofa_res = session.post(f"{BASE_URL}/twofa", data={
        "request_id": login_data['data']['request_id'],
        "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
        "user_id": login_data['data']['user_id'],
        "twofa_type": "totp"
    })
    twofa_res.raise_for_status()

    # Extract authentication token
    enctoken = session.cookies.get_dict().get("enctoken")
    return enctoken


def place_batch_order(enctoken):
    """Attempts to place multiple orders in a single request to check for batch order support."""
    url = "https://kite.zerodha.com/oms/orders/batch"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"enctoken {enctoken}"
    }

    batch_orders = [
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
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "squareoff": 0,
            "stoploss": 0,
            "trailing_stoploss": 0,
            "user_id": KITE_USERNAME
        },
        {
            "variety": "regular",
            "exchange": "NSE",
            "tradingsymbol": "RELIANCE",
            "transaction_type": "SELL",
            "order_type": "LIMIT",
            "quantity": 1,
            "price": 1700,
            "product": "MIS",
            "validity": "DAY",
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "squareoff": 0,
            "stoploss": 0,
            "trailing_stoploss": 0,
            "user_id": KITE_USERNAME
        }
    ]

    response = session.post(url, headers=headers, json=batch_orders)
    print(f"Batch Order Response: {response.json()}")


if __name__ == "__main__":
    enctoken = login()
    if enctoken:
        place_batch_order(enctoken)
