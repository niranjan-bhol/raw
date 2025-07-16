# Import the date object from the datetime module
from datetime import date

print("--- Storing USDINR Monthly Futures Expiry Dates for 2025 ---")

# Define variables for each month's expiry date in 2025
# Using the confirmed dates based on NSE data for 2025

usdinr_expiry_apr_2025 = date(2025, 4, 28)  # Monday
usdinr_expiry_may_2025 = date(2025, 5, 28)  # Wednesday
usdinr_expiry_jun_2025 = date(2025, 6, 26)  # Thursday
usdinr_expiry_jul_2025 = date(2025, 7, 29)  # Tuesday
usdinr_expiry_aug_2025 = date(2025, 8, 26)  # Tuesday
usdinr_expiry_sep_2025 = date(2025, 9, 26)  # Friday
usdinr_expiry_oct_2025 = date(2025, 10, 29) # Wednesday
usdinr_expiry_nov_2025 = date(2025, 11, 26) # Wednesday
usdinr_expiry_dec_2025 = date(2025, 12, 29) # Monday

# Print the stored dates for confirmation
print(f"\nStored Expiry Dates (YYYY-MM-DD):")
print(f"April 2025:    {usdinr_expiry_apr_2025}")
print(f"May 2025:      {usdinr_expiry_may_2025}")
print(f"June 2025:     {usdinr_expiry_jun_2025}")
print(f"July 2025:     {usdinr_expiry_jul_2025}")
print(f"August 2025:   {usdinr_expiry_aug_2025}")
print(f"September 2025:{usdinr_expiry_sep_2025}")
print(f"October 2025:  {usdinr_expiry_oct_2025}")
print(f"November 2025: {usdinr_expiry_nov_2025}")
print(f"December 2025: {usdinr_expiry_dec_2025}")

print("\n--------------------------------------------------------")