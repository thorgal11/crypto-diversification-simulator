from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time
from datetime import date
from currency_converter import CurrencyConverter
from pathlib import Path
import os


###############################################
# info
# this is an example of how to pull data from coinmarketcap for
# educational usage. the programm will request historical crypto price
# data of the first of every month and save the top 200 coins, their price
# in usd and eur in a csv file. sometimes the script wont get more data by the
# website so restart it, it will continue. use this data to simulate
# investments.
#
# pull data back to this year
last_year = 2015
###############################################


# pull data since first of actual month
year = date.today().year
month = date.today().month


c = CurrencyConverter(fallback_on_missing_rate=True,
                      fallback_on_wrong_date=True)
Path("csv/").mkdir(parents=True, exist_ok=True)

dates = []
print("\ncurrent date: " + str(year) + "  " + str(month) + "\n")

while year >= last_year:
    dates.append((month, year))
    month -= 1
    if month == 0:
        month = 12
        year -= 1

for d in dates:
    print("scraping 01 " + '{:02d}'.format(d[0]) + " " + str(d[1]) + ":")

    if os.path.isfile('csv/' + str(d[1]) + '_' + '{:02d}'.format(d[0])
                      + '_coinmarketcap.csv'):
        print("- data already exists -")
    else:
        datestr = str(d[1])+'{:02d}'.format(d[0])+'01'

        data = None

        while data is None:
            cmc = requests.get('https://coinmarketcap.com/historical/'
                               + datestr + '/')
            soup = BeautifulSoup(cmc.content, 'html.parser')
            data = soup.find('script',
                             id="__NEXT_DATA__",
                             type="application/json")
            if data is None:
                print("website doesnt respond - waiting 5s ..")
                time.sleep(5)

        coin_data = json.loads(data.contents[0])

        listings = coin_data['props']['initialState']['cryptocurrency']['listingHistorical']['data']

        name = []
        symbol = []
        slug = []
        usd = []
        eur = []
        rank = []
        market_cap = []

        df = pd.DataFrame(columns=['name', 'symbol', 'slug',
                          'usd', 'eur', 'market_cap', 'rank'])

        for i in listings:
            name.append(i['name'])
            symbol.append(i['symbol'])
            slug.append(i['slug'])
            usd.append(i['quote']['USD']['price'])
            eur.append(c.convert(i['quote']['USD']['price'], 'USD', 'EUR',
                                 date=date(d[1], d[0], 1)))
            market_cap.append(i['quote']['USD']['market_cap'])
            rank.append(i['rank'])

        if (i['rank'] != i['cmc_rank']):
            print("erröör!")

        df['name'] = name
        df['symbol'] = symbol
        df['slug'] = slug
        df['usd'] = usd
        df['eur'] = eur
        df['market_cap'] = market_cap
        df['rank'] = rank

        df.to_csv('csv/' + str(d[1]) + '_' + '{:02d}'.format(d[0])
                  + '_coinmarketcap.csv', index=False)

        print(df)
