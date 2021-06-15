# crypto-diversification-simulator
#### OR What if I invested 100€ every month in the top X coins of the time?
Im very interested in the idea of exchange-traded funds (ETF) for long time investments, as its minimizing the risk of traditional stock trading, brings solid interest and also doesnt require me to engage deeply with economics or buisnessplans of single companys.
The ongoing development of the cryptomarket of the last years made me curious, how it would've turned out if you'd applied this broad investment strategy there, and what would have been the best strategy:
Investing just in bitcoin? the top 20? top 50? top 100?
What if you'd have spent just 1€ on each of the top 100 coins every month?

## Getting started
### 1. Install modules
To run the code, install additional python modules:
```
pip install bs4 pandas requests currency_converter matplotlib numpy
```
### 2. Get historical data
To get historical price data to work on, run `scrape-top-200-per-month.py`
It will scrape data from coinmarketcap and save then in the folder csv/. Sometimes the website won't respond anymore, just restart the script to continue the progress. In this file you can set the last year to get data, by default it will try to download till 2015.

### 3. Simulate development of investment in detail
The script `crypto-investment-calculator.py` will use data in csv/ to simulate a diversificated crypto investment. You can setup the timespan, the amount of top coins to invest in and how much eur to invest every month. The program will display what coins will be in your wallet and their value.

### 4. Compare how diversification impacts on investment
This script will run simluate your investment divided in 1 - x coins and displays a graph for every month of the set timespan. The script is named `crypto-growth-factor-calculator.py`, it can be easily adjusted by the parameters in the beginning.

## Problems and Warning
The data scraped has prices in USD, but I used currency_converter to convert them to eur, which sometimes  isnt too exact. I checked back several results, but there might be issues or dates I didnt check which are distorting or totally erring the results.

Besides possible faulty results, this script is just simulating with historical data and and must in no way be seen as a prognosis of the future development of the cryptomarket - DONT USE RESULTS OF THIS SCRIPT AS INVESTMENT GUIDE. 
