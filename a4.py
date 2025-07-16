# Import necessary libraries
import yfinance as yf
import pandas as pd
from datetime import datetime

print("--- Fetching Latest Spot USD/INR using yfinance ---")

# Define the ticker symbol for USD/INR spot rate on Yahoo Finance
ticker_symbol = "USDINR=X"

# Get current time for reference
fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z') # Includes timezone if available
print(f"Attempting fetch at: {fetch_time}")

try:
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Attempt 1: Get data using the .info dictionary (might provide bid/ask/previous close)
    print(f"\nAttempt 1: Trying to get quote info via '.info' for {ticker_symbol}...")
    info = ticker.info

    # Check if useful keys exist in the info dictionary
    current_price = info.get('regularMarketPrice') # Sometimes available
    bid_price = info.get('bid')
    ask_price = info.get('ask')
    prev_close = info.get('previousClose')
    market_open = info.get('regularMarketOpen') # For reference

    got_info_price = False
    if bid_price and ask_price and bid_price != 0 and ask_price != 0:
        mid_price = (bid_price + ask_price) / 2
        print(f"  - Bid: {bid_price:.4f}")
        print(f"  - Ask: {ask_price:.4f}")
        print(f"  - Mid Price (Bid/Ask): {mid_price:.4f}")
        got_info_price = True
    elif current_price:
         print(f"  - Regular Market Price: {current_price:.4f}")
         got_info_price = True
    else:
        print("  - Current Bid/Ask or Market Price not found in '.info'.")

    if prev_close:
        print(f"  - Previous Close: {prev_close:.4f}")
    if market_open:
         print(f"  - Market Open: {market_open:.4f}")


    # Attempt 2: Fallback to fetching the last 1-minute data if .info wasn't sufficient
    if not got_info_price:
        print(f"\nAttempt 2: Fetching last available 1-minute closing price for {ticker_symbol}...")
        # Fetch 1-minute data for the last couple of days to ensure we get the latest tick
        # Note: 1m data is limited history, usually only last 7 days
        hist = ticker.history(period="2d", interval="1m")

        if not hist.empty:
            # Get the last available row/record
            last_record = hist.iloc[-1]
            last_price = last_record['Close']
            last_time = last_record.name # Timestamp is the index name

            print(f"  - Last 1-min Close Price: {last_price:.4f}")
            # Format timestamp if possible
            try:
                 print(f"  - Timestamp of Last Record: {last_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            except AttributeError:
                 print(f"  - Timestamp of Last Record: {last_time}") # Print as is if formatting fails
        else:
            print(f"  - Could not retrieve recent 1-minute historical data.")
            if prev_close:
                 print(f"  - Relying on Previous Close: {prev_close:.4f}")
            else:
                 print("  - No price data could be reliably fetched.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Could not fetch data. Check ticker symbol ('USDINR=X') and internet connection.")
    print("Note: yfinance relies on publicly available Yahoo Finance data which can have issues.")

print("\n--- Important Notes ---")
print("* Data is sourced from Yahoo Finance and may be delayed or aggregated.")
print("* It does not represent guaranteed interbank rates or official benchmarks like RBI/FBIL rates.")
print("* Accuracy and reliability are not guaranteed for trading purposes.")
print("------------------------")