from bs4 import BeautifulSoup
import requests

def fetch_term_sofr_1month_rate(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        rate_element = soup.select_one('table.table > tbody > tr:first-child > td:nth-child(2) > div.table-bold.text-end')
        if rate_element:
            return rate_element.text.strip().replace(" %", "")
        else:
            return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None

if __name__ == "__main__":
    us_int_url = "https://www.global-rates.com/en/interest-rates/cme-term-sofr/1/term-sofr-interest-1-month/"
    latest_int_rate = fetch_term_sofr_1month_rate(us_int_url)
    if latest_int_rate:
        print(f"The latest Term SOFR (1-month) is: {latest_int_rate} %")
    else:
        print("Could not fetch the 1-month term SOFR.")