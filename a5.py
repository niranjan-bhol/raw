# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import datetime

print("--- Fetching Spot USD/INR from CNBC Quote Page ---")

# URL for the CNBC quote page (likely USD/INR)
url = "https://www.cnbc.com/quotes/INR="
# Set headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Get current time for reference
fetch_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
print(f"Attempting fetch at: {fetch_time}")

try:
    # Send HTTP GET request to the URL
    response = requests.get(url, headers=headers, timeout=10) # Added timeout
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # --- Extract Data using the classes you identified ---

    # Find the Last Trade Time element
    time_element = soup.find('div', class_='QuoteStrip-lastTradeTime')
    # Find the Last Price element
    price_element = soup.find('span', class_='QuoteStrip-lastPrice')

    # Extract text if elements are found
    last_trade_time_text = "Not Found"
    last_price_text = "Not Found"

    if time_element:
        last_trade_time_text = time_element.get_text(strip=True)
        # Remove the "Last | " prefix if present
        if last_trade_time_text.startswith("Last | "):
             last_trade_time_text = last_trade_time_text[len("Last | "):].strip()
    else:
        print(" - Warning: Could not find the time element with class 'QuoteStrip-lastTradeTime'")

    if price_element:
        last_price_text = price_element.get_text(strip=True)
    else:
        print(" - Warning: Could not find the price element with class 'QuoteStrip-lastPrice'")

    # --- Print Results ---
    print("\n--- Fetched Data ---")
    print(f"Data Timestamp (on CNBC page): {last_trade_time_text}")
    print(f"Last Price: {last_price_text}")
    print("--------------------")

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred during the HTTP request: {e}")
except Exception as e:
    print(f"\nAn error occurred during parsing or processing: {e}")

print("\n--- Important Notes ---")
print("* This code scrapes the CNBC website. It WILL BREAK if CNBC changes its website structure/class names.")
print("* Use responsibly to avoid getting blocked.")
print("* Data timeliness depends on CNBC's website updates; accuracy depends on their Refinitiv feed.")
print("* This method is less reliable than using a dedicated API.")
print("------------------------")