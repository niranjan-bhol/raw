from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Optional

class INRRateFetcher:

    URL = "https://www.fbil.org.in/#/home"
    
    def __init__(self):
        self.url = INRRateFetcher.URL

    def fetch_term_mibor_rates(self) -> tuple[Optional[float], Optional[float], Optional[float], Optional[str]]:
        """
        Fetches the 14-day, 1-month, and 3-month MIBOR rates as floats,
        and the first available date as a string.
        """
        mibor_14d: Optional[float] = None
        mibor_1m: Optional[float] = None
        mibor_3m: Optional[float] = None
        first_date: Optional[str] = None
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(self.url)
                page.locator('a:has-text("MONEY MARKET/INTEREST RATES")').click()
                page.wait_for_timeout(1000)
                page.get_by_role("tab", name="Term MIBOR").click()
                page.wait_for_selector('#termmibor.active.show', timeout=15000)
                term_mibor_container_html = page.locator('#termmibor').inner_html()
                soup = BeautifulSoup(term_mibor_container_html, 'html.parser')
                tbody = soup.select_one('#termMibor tbody')

                if tbody:
                    rows = tbody.select('tr')
                    if rows:
                        first_row_cells = rows[0].select('td')
                        if first_row_cells and len(first_row_cells) > 0:
                            date_div = first_row_cells[0].select_one('div')
                            if date_div:
                                first_date = date_div.text.strip()

                    for row in rows[:3]:
                        cells = row.select('td')
                        if len(cells) == 5:
                            tenor_element = cells[1].select_one('div')
                            rate_element = cells[3].select_one('div')
                            if tenor_element and rate_element:
                                tenor = tenor_element.text.strip()
                                try:
                                    rate = float(rate_element.text.strip())
                                    if tenor == "14 DAYS":
                                        mibor_14d = rate
                                    elif tenor == "1 MONTH":
                                        mibor_1m = rate
                                    elif tenor == "3 MONTHS":
                                        mibor_3m = rate
                                except ValueError:
                                    # Skip or log if conversion to float fails
                                    continue
                
                browser.close()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return mibor_14d, mibor_1m, mibor_3m, first_date
