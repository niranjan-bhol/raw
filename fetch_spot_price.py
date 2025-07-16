import requests
from bs4 import BeautifulSoup
import datetime
from typing import Tuple, Optional

class SpotPriceFetcher:
    def __init__(self):
        # URL for the CNBC quote page (USD/INR)
        self.url = "https://www.cnbc.com/quotes/INR="

    def fetch_spot_price(self) -> Tuple[Optional[str], Optional[float]]:
        """
        Fetches the latest spot price and last trade time for USD/INR from CNBC.
        Returns:
            - last trade time (str)
            - last price (float)
        """
        # Get current time for reference
        fetch_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
        #print(f"Attempting fetch at: {fetch_time}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            # Send HTTP GET request to the URL
            response = requests.get(self.url, headers=headers, timeout=10)  # timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # --- Extract Data using the identified classes ---

            # Find the Last Trade Time element
            time_element = soup.find('div', class_='QuoteStrip-lastTradeTime')
            # Find the Last Price element
            price_element = soup.find('span', class_='QuoteStrip-lastPrice')

            # Extract text if elements are found
            last_trade_time_text = "Not Found"
            last_price_text = "Not Found"
            last_price_float = None

            if time_element:
                last_trade_time_text = time_element.get_text(strip=True)
                # Remove the "Last | " prefix if present
                if last_trade_time_text.startswith("Last | "):
                    last_trade_time_text = last_trade_time_text[len("Last | "):].strip()
            else:
                print(" - Warning: Could not find the time element with class 'QuoteStrip-lastTradeTime'")

            if price_element:
                last_price_text = price_element.get_text(strip=True)
                # Convert the price to a float
                try:
                    last_price_float = float(last_price_text.replace(',', ''))  # Remove commas, if any
                except ValueError:
                    print(" - Warning: Could not convert the last price to a float.")
            else:
                print(" - Warning: Could not find the price element with class 'QuoteStrip-lastPrice'")

            return last_trade_time_text, last_price_float

        except requests.exceptions.RequestException as e:
            print(f"\nAn error occurred during the HTTP request: {e}")
            return None, None
        except Exception as e:
            print(f"\nAn error occurred during parsing or processing: {e}")
            return None, None
