import yfinance as yf
from datetime import datetime
import numpy as np
import pandas as pd
import requests
import pyotp
from sklearn.linear_model import LinearRegression

import time
from datetime import datetime, timedelta

class TimeUtils:
    """Utility class for time-related functions."""
    
    @staticmethod
    def get_current_datetime_hh_mm_ss_ms():
        """Returns the current datetime with milliseconds."""
        return datetime.now()

    @staticmethod
    def get_current_datetime_hh_mm_ss():
        """Returns the current time in HH:MM:SS format."""
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def print_current_datetime_hh_mm_ss_ms():
        """Prints the current datetime with milliseconds."""
        print(TimeUtils.get_current_datetime_hh_mm_ss_ms().strftime("%H:%M:%S.%f"))

    @staticmethod
    def print_current_datetime_hh_mm_ss():
        """Prints the current time in HH:MM:SS format."""
        print(TimeUtils.get_current_datetime_hh_mm_ss())

    @staticmethod
    def execute_at_precise_time(target_time, func):
        """
        Executes a given function at a precise target time.

        :param target_time: Datetime object specifying the execution time.
        :param func: Function to execute.
        """
        delay = (target_time - datetime.now()).total_seconds()
        
        # Sleep until just before the target time
        time.sleep(max(0, delay - 0.1))
        
        # Busy-wait until the exact moment
        while datetime.now() < target_time:
            pass

        func()

class ETFPricePredictor:
    """Predicts ETF opening prices using linear regression based on underlying index data."""

    def __init__(self, assets, start_date="2025-01-01"):
        self.assets = assets
        self.start_date = start_date
        self.end_date = datetime.today().strftime("%Y-%m-%d")
        self.closing_prices = None
        self.opening_prices = {}
        self.models = {}

    def fetch_closing_prices(self):
        """Fetches daily closing prices for underlying indices and ETFs."""
        symbols = list(self.assets.keys()) + list(self.assets.values())  
        try:
            data = yf.download(symbols, start=self.start_date, end=self.end_date)["Close"]
            data.dropna(inplace=True)  
            self.closing_prices = data
        except Exception as e:
            print(f"Error fetching closing prices: {e}")

    def fetch_opening_prices(self):
        """Fetches today's opening prices for the underlying indices."""
        for index in self.assets.keys():
            try:
                data = yf.Ticker(index).history(period="1d")
                self.opening_prices[index] = data["Open"].iloc[0] if not data.empty else None
            except Exception as e:
                print(f"Error fetching opening price for {index}: {e}")
                self.opening_prices[index] = None  

    def train_models(self):
        """Trains a Linear Regression model for each ETF based on its underlying index."""
        if self.closing_prices is None:
            print("Error: Closing prices not available. Fetch data first.")
            return
        
        for index, etf in self.assets.items():
            try:
                X = self.closing_prices[index].values.reshape(-1, 1)  
                y = self.closing_prices[etf].values.reshape(-1, 1)  
                
                model = LinearRegression()
                model.fit(X, y)  
                self.models[etf] = model
            except Exception as e:
                print(f"Error training model for {etf}: {e}")

    def predict_opening_prices(self):
        """Predicts today's opening price for ETFs using the trained regression models."""
        predicted_openings = {}
        for index, etf in self.assets.items():
            if self.opening_prices.get(index) is not None and etf in self.models:
                try:
                    predicted_openings[etf] = self.models[etf].predict(np.array([[self.opening_prices[index]]]))[0][0]
                except Exception as e:
                    print(f"Error predicting opening price for {etf}: {e}")
                    predicted_openings[etf] = None
            else:
                predicted_openings[etf] = "Market Closed or Model Not Available"
        return predicted_openings

class ETFVolumeAnalyzer:
    """Analyzes ETF trading volume and calculates safe volume."""

    def __init__(self, assets, start_date="2025-01-01"):
        self.etf_symbols = list(assets.values())  
        self.start_date = start_date
        self.end_date = datetime.today().strftime("%Y-%m-%d")
        self.average_volumes = {}
        self.safe_volumes = {}

    def fetch_average_volumes(self):
        """Fetches daily ETF trading volumes and calculates the average volume for each ETF."""
        try:
            volume_data = yf.download(self.etf_symbols, start=self.start_date, end=self.end_date)["Volume"]
            self.average_volumes = volume_data.mean().to_dict()  
        except Exception as e:
            print(f"Error fetching ETF volumes: {e}")

    def calculate_safe_volumes(self):
        """Calculates safe volume using the formula: Average Volume / 4500."""
        for etf, avg_volume in self.average_volumes.items():
            self.safe_volumes[etf] = int(avg_volume / 4500)  
            # 6.25 hours = 22,500 seconds | 22500/5 = 4500

    def get_safe_volumes(self):
        """Returns the calculated safe volumes."""
        return self.safe_volumes

class ZerodhaLogin:
    """Handles Zerodha Kite login and maintains a session for order placement."""
    
    LOGIN_URL = "https://kite.zerodha.com/api/login"
    TOTP_URL = "https://kite.zerodha.com/api/twofa"

    def __init__(self, username, password, totp_key):
        self.username = username
        self.password = password
        self.totp_key = totp_key
        self.session = requests.Session()
        self.enctoken = None  
        self.headers = None  

    def login(self):
        """Performs login using Zerodha credentials and TOTP authentication."""
        try:
            res1 = self.session.post(self.LOGIN_URL, data={
                "user_id": self.username,
                "password": self.password,
                "type": "user_id"
            })
            res1.raise_for_status()  
            loginRes = res1.json()

            if "data" not in loginRes or "request_id" not in loginRes["data"]:
                raise ValueError("Login failed: Invalid response from server")

            totp_value = pyotp.TOTP(self.totp_key).now()
            finalRes = self.session.post(self.TOTP_URL, data={
                "request_id": loginRes["data"]["request_id"],
                "twofa_value": totp_value,
                "user_id": loginRes["data"]["user_id"],
                "twofa_type": "totp"
            })
            finalRes.raise_for_status()
            authRes = finalRes.json()

            if "status" not in authRes or authRes["status"] != "success":
                raise ValueError("TOTP Authentication failed")

            self.enctoken = self.session.cookies.get_dict().get("enctoken", None)
            if not self.enctoken:
                raise ValueError("Failed to retrieve enctoken")

            print("Login successful!")
            return self.session, self.enctoken

        except requests.exceptions.RequestException as e:
            print(f"HTTP Request Failed: {e}")
        except ValueError as ve:
            print(f"Error: {ve}")

class ZerodhaMargin:
    """Fetches margin details from Zerodha Kite API using an existing session."""

    MARGIN_URL = "https://kite.zerodha.com/oms/user/margins"

    def __init__(self, session, enctoken, headers):
        """Initialize with an existing authenticated session and headers."""
        self.session = session
        self.enctoken = enctoken
        self.headers = headers

        if not self.enctoken or not self.headers:
            raise ValueError("Authentication token or headers are missing. Cannot fetch margin data.")

    def fetch_margin(self):
        """Fetches margin details and extracts net margin for equity and commodity."""
        try:
            response = self.session.get(self.MARGIN_URL, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            equity_margin = data["data"]["equity"]["net"]
            commodity_margin = data["data"]["commodity"]["net"]

            return equity_margin, commodity_margin

        except requests.exceptions.RequestException as e:
            print(f"HTTP Request Failed: {e}")
            return None, None

class VolumeCalculation:
    """Calculates adjusted trading volumes based on margin and safe volumes."""

    def __init__(self, equity_margin, predicted_openings, safe_volumes):
        self.equity_margin = equity_margin
        self.predicted_openings = predicted_openings
        self.safe_volumes = safe_volumes

    def calculate_leveraged_margin(self):
        """Calculates leveraged margin as equity margin multiplied by 5."""
        return self.equity_margin * 5

    def calculate_discount_margin(self):
        """Calculates discounted margin as (equity margin * 5) - 5% of equity margin."""
        return (self.equity_margin * 5) - (self.equity_margin * 5 * 0.05)

    def calculate_trade_values(self):
        """Calculates trade value for each ETF as predicted_openings * safe_volumes."""
        return {etf: self.predicted_openings[etf] * self.safe_volumes[etf] for etf in self.safe_volumes}

    def calculate_total_trade_value(self, trade_values):
        """Calculates total trade value as the sum of all individual trade values."""
        return sum(trade_values.values())

    def calculate_allocation_ratio(self, discount_margin, total_trade_value):
        """Calculates allocation ratio as discount_margin / total_trade_value."""
        return discount_margin / total_trade_value if total_trade_value > 0 else 0

    def calculate_adjusted_quantities(self, allocation_ratio):
        """Calculates adjusted quantity for each ETF as allocation_ratio * safe_volumes."""
        return {etf: int(allocation_ratio * self.safe_volumes[etf]) for etf in self.safe_volumes}

    def execute_volume_calculation(self):
        """Executes all calculations and returns adjusted quantities."""
        discount_margin = self.calculate_discount_margin()  # Use discount margin instead of leveraged margin
        trade_values = self.calculate_trade_values()
        total_trade_value = self.calculate_total_trade_value(trade_values)
        allocation_ratio = self.calculate_allocation_ratio(discount_margin, total_trade_value)
        adjusted_quantities = self.calculate_adjusted_quantities(allocation_ratio)
        
        return adjusted_quantities

class DataStore:
    """Class to store symbols, adjusted quantities, and predicted prices."""

    def __init__(self):
        self.data = []

    def add_data(self, symbol, adjusted_quantity, predicted_price):
        """Adds a new entry to the data store."""
        self.data.append({
            'symbol_a': symbol,
            'quantity_a': adjusted_quantity,
            'price_a': predicted_price
        })

    def get_data(self):
        """Returns all stored data."""
        return self.data

class OrderStore:
    """Generates order data using symbols, quantities, and prices from DataStore."""

    def __init__(self):
        self.orders = []  # List to store order data

    def format_symbol(self, symbol):
        """Removes '.NS' from the symbol."""
        return symbol.split(".")[0]

    def add_order(self, symbol, quantity, price):
        """Creates two order records (BUY and SELL) for each ETF."""
        symbol_b = self.format_symbol(symbol)  # Format symbol
        price_b_buy = round(price * 0.95, 2)  # 0.5% lower for BUY
        price_b_sell = round(price * 1.05, 2)  # 0.5% higher for SELL
        quantity_b = quantity

        # Add BUY order
        self.orders.append({
            "symbol_b": symbol_b,
            "price_b": price_b_buy,
            "quantity_b": quantity_b,
            "txn_b": "BUY"
        })

        # Add SELL order
        self.orders.append({
            "symbol_b": symbol_b,
            "price_b": price_b_sell,
            "quantity_b": quantity_b,
            "txn_b": "SELL"
        })

    def generate_orders(self, data_store):
        """Creates orders from data stored in DataStore."""
        for entry in data_store.get_data():
            self.add_order(entry['symbol_a'], entry['quantity_a'], entry['price_a'])

    def get_orders(self):
        """Returns the list of generated orders."""
        return self.orders

class PayloadStore:
    """Stores order payloads in the required format."""

    def __init__(self):
        self.orders = []  # List to store formatted order payloads

    def add_order(self, symbol, txn, quantity, price):
        """Creates an order payload and adds it to the list."""
        order_payload = {
            "variety": "amo",
            "exchange": "NSE",
            "order_type": "LIMIT",
            "tradingsymbol": symbol,
            "transaction_type": txn,
            "quantity": quantity,
            "price": price,
            "product": "MIS",
            "validity": "IOC",
        }
        self.orders.append(order_payload)

    def generate_payloads(self, order_store):
        """Generates payloads from orders in OrderStore."""
        for order in order_store.get_orders():
            self.add_order(
                symbol=order["symbol_b"],
                txn=order["txn_b"],
                quantity=order["quantity_b"],
                price=order["price_b"]
            )

    def get_payloads(self):
        """Returns the generated payloads."""
        return self.orders

class ZerodhaOrders:
    """Handles synchronous order placement using requests."""

    ORDER_URL = "https://kite.zerodha.com/oms/orders/regular"

    def __init__(self, session, enctoken, headers):
        """Initialize with an existing authenticated session and headers."""
        self.session = session
        self.enctoken = enctoken
        self.headers = headers

        if not self.enctoken or not self.headers:
            raise ValueError("Authentication token or headers are missing. Cannot place orders.")

    def place_order(self, order_data):
        """Places a single order synchronously."""
        try:
            response = requests.post(self.ORDER_URL, headers=self.headers, data=order_data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def place_orders(self, order_payloads):
        """Places multiple orders synchronously."""
        results = []
        for order in order_payloads:
            result = self.place_order(order)
            results.append(result)
        return results

def main():
    """Main execution function"""
    assets = {
        "^NSEI": "NIFTYBEES.NS",      # Nifty 50 → Niftybees
        "^NSMIDCP": "JUNIORBEES.NS",   # Nifty Next 50 → Junior Bees
        "^NSEBANK": "BANKBEES.NS"      # Nifty Bank → Bank Bees
    }

    # Predict ETF opening prices
    predictor = ETFPricePredictor(assets)
    
    print("Fetching historical closing prices...")
    predictor.fetch_closing_prices()

    print("Fetching today's opening prices...")
    predictor.fetch_opening_prices()

    print("Training regression models...")
    predictor.train_models()

    print("\nToday's Opening Prices:")
    for index, price in predictor.opening_prices.items():
        print(f"{index}: {price}")

    print("\nPredicted ETF Opening Prices:")
    predicted_prices = predictor.predict_opening_prices()
    for etf, price in predicted_prices.items():
        print(f"{etf}: {price:.2f}" if isinstance(price, float) else f"{etf}: {price}")

    # Analyze ETF trading volumes
    volume_analyzer = ETFVolumeAnalyzer(assets)
    
    print("\nFetching ETF volume data...")
    volume_analyzer.fetch_average_volumes()

    print("Calculating safe volumes...")
    volume_analyzer.calculate_safe_volumes()

    print("\nAverage ETF Trading Volumes:")
    for etf, avg_volume in volume_analyzer.average_volumes.items():
        print(f"{etf}: {avg_volume:,.0f}")

    print("\nSafe Trading Volumes:")
    safe_volumes = volume_analyzer.get_safe_volumes()
    for etf, safe_vol in safe_volumes.items():
        print(f"{etf}: {safe_vol}")

    # Log in to Zerodha
    zerodha = ZerodhaLogin("DXU151", "Pratibha", "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP")
    session, enctoken = zerodha.login()

    # Ensure successful login before proceeding
    if not enctoken:
        print("Zerodha login failed. Exiting...")
        return  

    # Initialize ZerodhaMargin with correct headers
    headers = {
        "Authorization": f"enctoken {enctoken}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
    }

    zerodha_margin = ZerodhaMargin(session, enctoken, headers)
    equity_margin, commodity_margin = zerodha_margin.fetch_margin()

    print("\nZerodha Margin Details:")
    print(f"Equity Margin: {equity_margin}")
    print(f"Commodity Margin: {commodity_margin}")

    # Initialize VolumeCalculation with necessary data
    volume_calculator = VolumeCalculation(equity_margin, predicted_prices, safe_volumes)

    # Calculate adjusted quantities
    adjusted_quantities = volume_calculator.execute_volume_calculation()

    print("\nAdjusted Quantities for Each ETF:")
    for etf, adjusted_quantity in adjusted_quantities.items():
        print(f"{etf}: {adjusted_quantity}")

    # Create DataStore and add data
    datastore = DataStore()
    
    for etf, adjusted_quantity in adjusted_quantities.items():
        predicted_price = predicted_prices.get(etf, None)
        datastore.add_data(etf, adjusted_quantity, predicted_price)

    # Get and display the stored data
    print("\nStored Data:")
    data = datastore.get_data()
    for entry in data:
        print(f"Symbol: {entry['symbol_a']}, Quantity: {entry['quantity_a']}, Predicted Price: {entry['price_a']}")

    # Create an instance of OrderStore
    order_store = OrderStore()

    # Generate orders using data from DataStore
    order_store.generate_orders(datastore)

    # Retrieve and display the orders
    print("\nGenerated Orders:")
    for order in order_store.get_orders():
        print(f"Symbol: {order['symbol_b']}, Price: {order['price_b']}, Quantity: {order['quantity_b']}, TXN: {order['txn_b']}")

    # Create an instance of PayloadStore
    payload_store = PayloadStore()

    # Generate payloads from orders
    payload_store.generate_payloads(order_store)

    # Retrieve and display the payloads
    print("\nGenerated Payloads:")
    for payload in payload_store.get_payloads():
        print(payload)

    order_payloads = payload_store.get_payloads()  # Get the actual data

    # Initialize ZerodhaOrders
    zerodha_orders = ZerodhaOrders(session, enctoken, headers)

    # Place orders
    results = zerodha_orders.place_orders(order_payloads)

    # Define the exact target time
    now = datetime.now()
    target_time = now.replace(hour=9, minute=15, second=0, microsecond=0)

    def execute_orders():
        """Function to place orders precisely at 9:15 AM"""
        # Assuming session, enctoken, and headers are already initialized
        #zerodha_orders = ZerodhaOrders(session, enctoken, headers)
        #order_payloads = payload_store.get_payloads()
        results = zerodha_orders.place_orders(order_payloads)
            
        # Print results
        #print("\nOrder Placement Results:", results)

    # Execute `execute_orders` at exactly 9:15 AM
    TimeUtils.execute_at_precise_time(target_time, execute_orders)

    # Print responses
    print("\nOrder Placement Results:", results)

if __name__ == "__main__":
    main()
