# To check which ETFs are allowed for intraday trading

import pyotp
import requests

# Credentials
KITE_USERNAME = "DXU151"
KITE_PASSWORD = "Pratibha"
TOTP_KEY = "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP"

# Zerodha API URLs
BASE_URL = "https://kite.zerodha.com/api"
ORDER_URL = "https://kite.zerodha.com/oms/orders/regular"

# List of trading symbols
symbols = [
    "ABGSEC", "ABSLBANETF", "ABSLLIQUID", "ABSLNN50ET", "ABSLPSE", "ALPHA", "ALPHAETF", "ALPL30IETF", "AUTOBEES",
    "AUTOIETF", "AXISBNKETF", "AXISBPSETF", "AXISCETF", "AXISGOLD", "AXISHCETF", "AXISILVER", "AXISNIFTY",
    "AXISTECETF", "AXSENSEX", "BANKBEES", "BANKBETF", "BANKETF", "BANKETFADD", "BANKIETF", "BANKNIFTY1", "BANKPSU",
    "BBETF0432", "BBNPNBETF", "BBNPPGOLD", "BFSI", "BSE500IETF", "BSLGOLDETF", "BSLNIFTY", "BSLSENETFG", "COMMOIETF",
    "CONS", "CONSUMBEES", "CONSUMER", "CONSUMIETF", "CPSEETF", "DIVOPPBEES", "EBANKNIFTY", "EBBETF0425", "EBBETF0430",
    "EBBETF0431", "EBBETF0433", "ECAPINSURE", "EGOLD", "EMULTIMQ", "EQUAL50ADD", "ESG", "ESILVER", "EVINDIA",
    "FINIETF", "FMCGIETF", "GILT5YBEES", "GOLD1", "GOLDBEES", "GOLDCASE", "GOLDETF", "GOLDETFADD", "GOLDIETF",
    "GOLDSHARE", "GROWWDEFNC", "GROWWEV", "GROWWGOLD", "GROWWLIQID", "GROWWRAIL", "GSEC10ABSL", "GSEC10IETF",
    "GSEC10YEAR", "GSEC5IETF", "HDFCBSE500", "HDFCGOLD", "HDFCGROWTH", "HDFCLIQUID", "HDFCLOWVOL", "HDFCMID150",
    "HDFCMOMENT", "HDFCNEXT50", "HDFCNIF100", "HDFCNIFBAN", "HDFCNIFIT", "HDFCNIFTY", "HDFCPSUBK", "HDFCPVTBAN",
    "HDFCQUAL", "HDFCSENSEX", "HDFCSILVER", "HDFCSML250", "HDFCVALUE", "HEALTHADD", "HEALTHIETF", "HEALTHY",
    "HNGSNGBEES", "ICICIB22", "IDFNIFTYET", "INFRABEES", "INFRAIETF", "IT", "ITBEES", "ITETF", "ITETFADD", "ITIETF",
    "IVZINGOLD", "IVZINNIFTY", "JUNIORBEES", "LICMFGOLD", "LICNETFGSC", "LICNETFN50", "LICNETFSEN", "LICNFNHGP",
    "LICNMID100", "LIQUID", "LIQUID1", "LIQUIDADD", "LIQUIDBEES", "LIQUIDBETF", "LIQUIDCASE", "LIQUIDETF",
    "LIQUIDIETF", "LIQUIDPLUS", "LIQUIDSBI", "LIQUIDSHRI", "LOWVOL", "LOWVOL1", "LOWVOLIETF", "LTGILTBEES",
    "MAFANG", "MAHKTECH", "MAKEINDIA", "MASPTOP50", "METAL", "METALIETF", "MID150BEES", "MID150CASE", "MIDCAP",
    "MIDCAPETF", "MIDCAPIETF", "MIDQ50ADD", "MIDSELIETF", "MIDSMALL", "MNC", "MODEFENCE", "MOGSEC", "MOHEALTH",
    "MOLOWVOL", "MOM100", "MOM30IETF", "MOM50", "MOMENTUM", "MOMENTUM50", "MOMOMENTUM", "MON100", "MONIFTY500",
    "MONQ50", "MOQUALITY", "MOREALTY", "MOSMALL250", "MOVALUE", "MULTICAP", "NETF", "NEXT30ADD", "NEXT50",
    "NEXT50IETF", "NIF100BEES", "NIF100IETF", "NIF10GETF", "NIF5GETF", "NIFITETF", "NIFMID150", "NIFTY1",
    "NIFTY50ADD", "NIFTYBEES", "NIFTYBETF", "NIFTYETF", "NIFTYIETF", "NIFTYQLITY", "NPBET", "NV20", "NV20BEES",
    "NV20IETF", "OILIETF", "PHARMABEES", "PSUBANK", "PSUBANKADD", "PSUBNKBEES", "PSUBNKIETF", "PVTBANIETF",
    "PVTBANKADD", "QGOLDHALF", "QNIFTY", "QUAL30IETF", "SBIETFCON", "SBIETFIT", "SBIETFPB", "SBIETFQLTY",
    "SBINEQWETF", "SBISILVER", "SDL26BEES", "SENSEXADD", "SENSEXETF", "SENSEXIETF", "SETF10GILT", "SETFGOLD",
    "SETFNIF50", "SETFNIFBK", "SETFNN50", "SHARIABEES", "SILVER", "SILVER1", "SILVERADD", "SILVERBEES",
    "SILVERETF", "SILVERIETF", "SILVRETF", "SMALLCAP", "TATAGOLD", "TATSILV", "TECH", "TNIDETF", "TOP100CASE",
    "TOP10ADD", "UTIBANKETF", "UTINEXT50", "UTINIFTETF", "UTISENSETF", "UTISXN50", "VAL30IETF"
]

# Initialize session
session = requests.Session()

def login():
    """Logs in to Zerodha and returns authentication token."""
    res1 = session.post(f"{BASE_URL}/login", data={"user_id": KITE_USERNAME, "password": KITE_PASSWORD, "type": "user_id"})
    login_data = res1.json()

    twofa_res = session.post(f"{BASE_URL}/twofa", data={
        "request_id": login_data['data']['request_id'],
        "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
        "user_id": login_data['data']['user_id'],
        "twofa_type": "totp"
    })

    # Extract authentication token
    enctoken = session.cookies.get_dict().get("enctoken")
    return enctoken if enctoken else None

def place_orders(enctoken):
    """Places multiple orders for different symbols."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"enctoken {enctoken}"
    }

    for symbol in symbols:
        order_data = {
            "variety": "regular",
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "transaction_type": "BUY",
            "order_type": "LIMIT",
            "quantity": 1,
            "price": 1000,
            "product": "MIS",
            "validity": "DAY"
        }
        response = session.post(ORDER_URL, headers=headers, data=order_data)
        print(f"Order for {symbol}: {response.json()}")

if __name__ == "__main__":
    enctoken = login()
    if enctoken:
        place_orders(enctoken)
