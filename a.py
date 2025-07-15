# Zerodha Login & Order Placement Data For Traders Code Jupyter Notebook

KITE_USERNAME = 'DXU151'
KITE_PASSWORD = 'Pratibha'
TOTP_KEY      = 'FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP'

# ----------------------------------------------------------------------------------------------------

import pyotp,requests
session = requests.Session()

res1 = session.post('https://kite.zerodha.com/api/login', data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD ,"type" :"user_id"})
loginRes = res1.json()  
loginRes

# ----------------------------------------------------------------------------------------------------

finalRes = session.post('https://kite.zerodha.com/api/twofa', data={"request_id": loginRes['data']['request_id'],
    "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
    "user_id": loginRes['data']['user_id'],
    "twofa_type":"totp"                                                                 
})
finalRes.json()

# ----------------------------------------------------------------------------------------------------

cookiesDict = session.cookies.get_dict()
cookiesDict

# ----------------------------------------------------------------------------------------------------

enctoken = cookiesDict['enctoken']
enctoken

# ----------------------------------------------------------------------------------------------------

import requests
url = 'https://kite.zerodha.com/oms/orders/regular'

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
        'Authorization': f"enctoken {enctoken}"
}

order_data = {
    "variety": "vtujyvybilk",
    "exchange": "NSE",
    "tradingsymbol": "IDEA",
    "transaction_type": "BUY",
    "order_type": "MARKET",
    "quantity": 1,
    "product": "MIS",
    "validity": "DAY",
    "user_id": KITE_USERNAME
}

orderes = requests.post(url,headers= headers,data =order_data)
orderes.json()
print(orderes.json())

# ----------------------------------------------------------------------------------------------------

