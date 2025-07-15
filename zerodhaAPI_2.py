import pyotp
import requests

# Credentials (Keep these secure, avoid hardcoding in production)
KITE_USERNAME = "DXU151"
KITE_PASSWORD = "Pratibha"
TOTP_KEY = "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP"

BASE_URL = "https://kite.zerodha.com/api"

# Initialize session
session = requests.Session()

def login():
    """Logs in to Zerodha and returns the session with authentication."""
    try:
        # Step 1: Send login request
        res1 = session.post(f"{BASE_URL}/login", data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"})
        res1.raise_for_status()
        login_data = res1.json()

        # Step 2: Perform two-factor authentication (TOTP)
        twofa_res = session.post(f"{BASE_URL}/twofa", data={
            "request_id": login_data['data']['request_id'],
            "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
            "user_id": login_data['data']['user_id'],
            "twofa_type": "totp"
        })
        twofa_res.raise_for_status()
        print("Login successful")

        # Extract authentication token
        enctoken = session.cookies.get_dict().get("enctoken")
        if not enctoken:
            print("Failed to retrieve authentication token.")
            return None
        
        return enctoken

    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        return None


def place_order(enctoken):
    """Places an order on Zerodha."""
    try:
        url = "https://kite.zerodha.com/oms/orders/regular"
        
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
        }

        # Send order request
        response = session.post(url, headers=headers, data=order_data)
        response.raise_for_status()
        
        order_response = response.json()
        print(f"Order placed successfully: {order_response}")
        return order_response

    except requests.exceptions.RequestException as e:
        print(f"Order placement failed: {e}")
        return None


if __name__ == "__main__":
    enctoken = login()
    if enctoken:
        place_order(enctoken)
