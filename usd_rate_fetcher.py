import requests
from bs4 import BeautifulSoup
from typing import Optional

class USDRateFetcher:
    def __init__(self):
        self.url = "https://www.global-rates.com/en/interest-rates/cme-term-sofr/1/term-sofr-interest-1-month/"

    def fetch_term_sofr_1month_rate(self) -> Optional[float]:
        """
        Fetches the 1-month term SOFR rate from the predefined URL as a float.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            rate_element = soup.select_one('table.table > tbody > tr:first-child > td:nth-child(2) > div.table-bold.text-end')

            if rate_element:
                rate_str = rate_element.text.strip().replace(" %", "")
                return float(rate_str)
            return None
        except (requests.exceptions.RequestException, ValueError):
            return None
        except Exception:
            return None
