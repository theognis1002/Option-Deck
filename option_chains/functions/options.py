import requests
from pprint import pprint
import pandas as pd
from statistics import mean
import numpy as np
from datetime import datetime, timedelta
import quandl
from config import tradier_token, quandl_token


quandl.ApiConfig.api_key = quandl_token

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None

todays_date = datetime.utcnow().strftime("%Y-%m-%d")
last_weekday = datetime.utcnow() if datetime.utcnow().weekday() < 5 \
    else datetime.utcnow() - timedelta(days=datetime.utcnow().weekday() - 4)


def treasury_rates():
    rates = quandl.get('USTREASURY/YIELD', start_date=last_weekday, end_date=last_weekday)
    risk_free_rate = rates['10 YR']
    print(rates)
    return risk_free_rate, rates


def get_quote(ticker):
    response = requests.get('https://api.tradier.com/v1/markets/quotes',
                            params={'symbols': f'{ticker}', 'greeks': 'false'},
                            headers={'Authorization': f'Bearer {tradier_token}', 'Accept': 'application/json'}
                            )
    json_response = response.json()
    results = json_response['quotes']['quote']
    print(f"Price: ${results['last']}/share \n"
          f"+/-: {results['change_percentage']}%")

    return results


def option_expirations(ticker):
    response = requests.get('https://api.tradier.com/v1/markets/options/expirations',
                            params={'symbol': f'{ticker}', 'includeAllRoots': 'true', 'strikes': 'true'},
                            headers={'Authorization': f'Bearer {tradier_token}', 'Accept': 'application/json'}
                            )
    json_response = response.json()
    results = json_response['expirations']['expiration']
    return results


def option_chains(ticker, expiration_dates):
    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
                            params={'symbol': f'{ticker}', 'expiration': f'{expiration_dates}', 'greeks': 'true'},
                            headers={'Authorization': f'Bearer {tradier_token}', 'Accept': 'application/json'}
                            )
    json_response = response.json()
    results = json_response['options']['option']
    return results


def option_alt_source():
    """ alternative option chain data source from Yahoo Finance """
    chain = options.get_options_chain('AAPL')
    pprint(chain)


def short_option_scanner(ticker):
    expirations = option_expirations(ticker)
    for expiration in expirations:
        date = expiration['date']
        chains = option_chains(ticker, date)
        chains = [chain for chain in chains if chain['option_type'] == 'put']

        for chain in reversed(chains):
            option_type = chain['option_type']
            expiration_date = chain['expiration_date']
            try:
                contract_price = float(chain['last']) * 100
            except TypeError as e:
                # print(e.__class__.__name__, str(e), sep=" - ")
                contract_price = mean([float(chain['ask']), float(chain['bid'])])
            strike = chain['strike']
            premium_yield = round((contract_price / strike) * 100, 2)
            volume = chain['volume']
            open_interest = chain['open_interest']
            iv = chain['greeks']['ask_iv']
            print("exp date:", expiration_date)
            print("Contract Price:", contract_price)
            print("volume:", volume)
            print("open_interest:", open_interest)
            print("premium_yield:", str(premium_yield) + "%")
            print("strike price:", strike)
            print("IV:", iv)
            print("-"*50)


if __name__ == '__main__':
    short_option_scanner('FB')
