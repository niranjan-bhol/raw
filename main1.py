import pyotp
import requests
import payload1

# Credentials (Move to environment variables in production)
KITE_USERNAME = "DXU151"
KITE_PASSWORD = "Pratibha"
TOTP_KEY = "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP"

BASE_URL = "https://kite.zerodha.com/api"
ORDER_URL = "https://kite.zerodha.com/oms/orders/regular"

# Initialize session
session = requests.Session()

def login():
    """Logs in to Zerodha and returns the authentication token."""
    try:
        res1 = session.post(
            f"{BASE_URL}/login", 
            data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"}
        )
        res1.raise_for_status()
        login_data = res1.json()

        request_id = login_data.get("data", {}).get("request_id")
        user_id = login_data.get("data", {}).get("user_id")
        if not request_id or not user_id:
            print("Login failed: Missing request_id or user_id")
            return None

        # Perform two-factor authentication (TOTP)
        twofa_res = session.post(
            f"{BASE_URL}/twofa", 
            data={
                "request_id": request_id,
                "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
                "user_id": user_id,
                "twofa_type": "totp"
            }
        )
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


def place_order(enctoken, order_data):
    """Places an order on Zerodha."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://kite.zerodha.com/dashboard",
            "Accept-Language": "en-US,en;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"enctoken {enctoken}"
        }

        # Send order request
        response = session.post(ORDER_URL, headers=headers, data=order_data)
        response.raise_for_status()
        
        order_response = response.json()
        print(f"Order placed: {order_response}")
        return order_response

    except requests.exceptions.RequestException as e:
        print(f"Order placement failed: {e}")
        return None


if __name__ == "__main__":
    enctoken = login()
    if enctoken:
        for order in payload1.orders:
            place_order(enctoken, order)
