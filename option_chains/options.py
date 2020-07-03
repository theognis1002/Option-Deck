from datetime import datetime, timedelta
from pprint import pprint
from statistics import mean
from config import tradier_token, quandl_token
import pandas as pd
import quandl
import requests
from bs4 import BeautifulSoup


quandl.ApiConfig.api_key = quandl_token

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.options.mode.chained_assignment = None

start_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
end_date = datetime.utcnow().strftime("%Y-%m-%d")


def treasury_rates():
    rates = quandl.get("USTREASURY/YIELD", start_date=start_date, end_date=end_date)
    rates = rates.to_json()
    return rates


def get_quote(ticker):
    response = requests.get(
        "https://api.tradier.com/v1/markets/quotes",
        params={"symbols": f"{ticker}", "greeks": "false"},
        headers={
            "Authorization": f"Bearer {tradier_token}",
            "Accept": "application/json",
        },
    )
    json_response = response.json()
    results = json_response
    return results


def option_expirations(ticker):
    response = requests.get(
        "https://api.tradier.com/v1/markets/options/expirations",
        params={"symbol": f"{ticker}", "includeAllRoots": "true", "strikes": "true"},
        headers={
            "Authorization": f"Bearer {tradier_token}",
            "Accept": "application/json",
        },
    )
    json_response = response.json()
    results = json_response["expirations"]["expiration"]
    return results


def option_chains(ticker, expiration_dates):
    response = requests.get(
        "https://api.tradier.com/v1/markets/options/chains",
        params={
            "symbol": f"{ticker}",
            "expiration": f"{expiration_dates}",
            "greeks": "true",
        },
        headers={
            "Authorization": f"Bearer {tradier_token}",
            "Accept": "application/json",
        },
    )
    json_response = response.json()
    results = json_response["options"]["option"]
    return results


def option_alt_source():
    """ alternative option chain data source from Yahoo Finance """
    chain = option_chains("AAPL")
    print(chain)


def short_option_scanner(ticker, option_type):
    option_type = option_type.lower()
    expirations = option_expirations(ticker)
    ticker_chain = []
    for expiration in expirations[:2]:
        date = expiration["date"]
        chains = option_chains(ticker, date)
        ticker_chain.append(chains)
    print(ticker_chain)
    return ticker_chain


def scraper():
    r = requests.get('https://www.gurufocus.com/stock/ma/summary')
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.find("div", {"class": "summary-section-lg"}))

if __name__ == "__main__":
    scraper()
