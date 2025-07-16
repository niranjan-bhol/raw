from calc_e import get_e_value
from usd_rate_fetcher import USDRateFetcher
from inr_rate_fetcher import INRRateFetcher
from fetch_spot_price import SpotPriceFetcher
from expiry_dates import USDINRExpiryDates2025
from fetch_time_to_expiry import TimeToExpiryCalculator
from datetime import datetime

def main():

    print()

    e_value = get_e_value()
    print(f"The value of Euler's number (e) is: {e_value}")

    print()

    days_remaining = TimeToExpiryCalculator.calculate_days_to_expiry()
    print(f"Days to expiry for this month's USDINR futures contract: {days_remaining}")

    print()

    fetcher = USDRateFetcher()
    latest_int_rate = fetcher.fetch_term_sofr_1month_rate()
    
    if latest_int_rate:
        print(f"The latest Term SOFR (1-month) is: {latest_int_rate} %")
    #else:
        #print("Could not fetch the 1-month term SOFR.")
    
    print()

    fetcher = INRRateFetcher()
    mibor_14d_rate, mibor_1m_rate, mibor_3m_rate, date = fetcher.fetch_term_mibor_rates()
    
    print(f"MIBOR Rates | {date}")
    print(f"var1 : 14 Days  : {mibor_14d_rate} %")
    print(f"var2 : 1 Month  : {mibor_1m_rate} %")
    print(f"var3 : 3 Months : {mibor_3m_rate} %")

    print()

    spot_price_fetcher = SpotPriceFetcher()
    
    last_trade_time, last_price = spot_price_fetcher.fetch_spot_price()
    
    if last_trade_time and last_price is not None:
        now = datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"USDINR Spot Data | {formatted_datetime}")
        print(f"Data Timestamp (on CNBC page): {last_trade_time}")
        print(f"Last Price: {last_price:.4f}")
    else:
        print("Could not fetch any spot price data.")

    print()

    e = e_value
    T = days_remaining/365
    r_f = latest_int_rate/100
    r_d = mibor_1m_rate/100
    #S = last_price
    S = 85.6543
    
    #F1 = S * e^((r_d - r_f) * T)
    F2 = S * e ** ((r_d - r_f) * T)
    #F3 = S * (1 + (r_d - r_f) * T)
    #F4 = S * 1 + ((r_d - r_f) * T)
    
    print(f"Fair price of USDINR : {F2:.4f}")

    print()

if __name__ == "__main__":
    main()
