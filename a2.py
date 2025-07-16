from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Optional

def fetch_term_mibor_rates(url: str) -> tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    mibor_14d: Optional[str] = None
    mibor_1m: Optional[str] = None
    mibor_3m: Optional[str] = None
    first_date: Optional[str] = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
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
                            rate = rate_element.text.strip()
                            if tenor == "14 DAYS":
                                mibor_14d = rate
                            elif tenor == "1 MONTH":
                                mibor_1m = rate
                            elif tenor == "3 MONTHS":
                                mibor_3m = rate
            browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    return mibor_14d, mibor_1m, mibor_3m, first_date

if __name__ == "__main__":
    us_int_url = "https://www.fbil.org.in/#/home"
    mibor_14d_rate, mibor_1m_rate, mibor_3m_rate, date = fetch_term_mibor_rates(us_int_url)

    print(f"Date: {date}")
    print("--- MIBOR Rates ---")
    print(f"var1 : mibor_14d: {mibor_14d_rate}")
    print(f"var2 : mibor_1m: {mibor_1m_rate}")
    print(f"var3 : mibor_3m: {mibor_3m_rate}")