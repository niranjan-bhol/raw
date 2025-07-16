# info.py
"""
Information hub for the USDINR Futures Fair Value Calculation project.
Documents the core formula, variable definitions, and chosen data sources.

Date Created/Updated: 2025-04-18
"""

# -----------------------------------------------------------------------------
# Core Formula: Interest Rate Parity (Continuous Compounding)
# -----------------------------------------------------------------------------
# F = S * e^((rd - rf) * T)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Variable Definitions and Data Sources
# -----------------------------------------------------------------------------

# F: Fair Future Price
#    - Full Name: Theoretical Fair Value of the USDINR Futures Contract
#    - Description: The calculated 'ideal' price based on IRP.
#    - Source: This is the output of the calculation.

# S: Spot Exchange Rate
#    - Full Name: Spot USD/INR Exchange Rate
#    - Description: Current market rate for exchanging USD to INR.
#    - Source: Real-time feed providing quotes like "INR=:Exchange".
#      (Likely sourced from a professional data vendor such as
#      Refinitiv or Bloomberg via a specific terminal or API feed).
#      Accuracy/Latency Note: Requires a low-latency, reliable feed.

# e: Euler's Number
#    - Full Name: Euler's Number (Base of the Natural Logarithm)
#    - Description: Mathematical constant (~2.71828...).
#    - Source: Python's standard `math` module (accessed via `math.e`
#      or used implicitly within the `math.exp()` function).

# rd: Domestic Risk-Free Interest Rate (INR)
#    - Full Name: Indian Rupee Risk-Free Interest Rate (Annualized)
#    - Description: Rate representing risk-free return in INR for tenor T.
#    - Chosen Proxy: Term MIBOR (Mumbai Interbank Offer Rate).
#    - Chosen Tenor: 1-Month Term MIBOR (considered best practical fit for near-month futures).
#    - Source: Scraped from FBIL website (https://www.fbil.org.in/#/home) using the
#      Playwright script (`fbil_scraper.py`).
#    - Reliability Note: Scraping is fragile and may break if the website changes.
#      Data timeliness depends on website updates and scraping execution.

# rf: Foreign Risk-Free Interest Rate (USD)
#    - Full Name: US Dollar Risk-Free Interest Rate (Annualized)
#    - Description: Rate representing risk-free return in USD for tenor T.
#    - Chosen Proxy: Term SOFR (Secured Overnight Financing Rate).
#    - Chosen Tenor: 1-Month Term SOFR (market standard, forward-looking).
#    - Source: Scraped from Global-Rates.com (https://www.global-rates.com/en/interest-rates/cme-term-sofr/1/term-sofr-interest-1-month/)
#      using the scraping script (`rate_fetcher.py` - concise version).
#    - Reliability Note: Scraping is fragile and may break if the website changes.
#      Rate is published once daily (US time). Official sources like CME API or
#      vendors are more reliable.

# T: Time to Expiry
#    - Full Name: Time to Expiry (in years)
#    - Description: Remaining time until the specific futures contract expires,
#      expressed as a fraction of a year.
#    - Source: Calculated based on the current date and the official expiry date
#      of the specific USDINR futures contract being priced.
#    - Expiry Date Source: National Stock Exchange (NSE) India website for
#      official contract specifications.
#    - Calculation: T = (Expiry Date - Current Date).days / 365.0 (using 365 days)

# -----------------------------------------------------------------------------
# End of Information
# -----------------------------------------------------------------------------