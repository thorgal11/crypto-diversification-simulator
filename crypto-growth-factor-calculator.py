import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###############################################
# info
# set the timespan of your investment and the max. number
# of coins you want to invest in. the programm calculates
# the development of you investment regarding the amount
# of coins you invested in and displays every month as a line
# in the graph
#
# set your parameters here:
#
# starting which months
start_month = 1
start_year = 2019
# investing till
end_month = 1
end_year = 2021
# divide investment by 1 - max_diversification coins
max_diversification = 50
# show detailed output which coins have been bought
# just reasonable for months = 1
show_investments = False
###############################################


def calculate_growth(
    start_month, start_year,
    months_of_investment,
    invested_cryptos
):

    invest_per_month = 100
    invested_usd = 0
    wallet = {}

    year = start_year
    month = start_month

    while True:
        if show_investments:
            print("\nCalculating Date: " + str(month) + " " + str(year) + "\n")

        # increase investment
        invested_usd += invest_per_month

        # import selected crypto toplist
        data = pd.read_csv('csv/'+str(year)+'_'
                           + '{:02d}'.format(month)
                           + '_coinmarketcap.csv',
                           nrows=invested_cryptos)
        df = pd.DataFrame(data, columns=['name', 'usd'])

        for i in range(len(df)):
            crypto_name = df.loc[i, 'name']
            crypto_price = float(df.loc[i, 'usd'])
            share = (invest_per_month / invested_cryptos) / crypto_price

            if show_investments:
                print("Buying " + crypto_name.ljust(18)
                      + " at price of " + "{:10.5f}".format(crypto_price).ljust(15)
                      + "\tshare: " "{:10.5f}".format(share))

            if crypto_name in wallet:
                wallet[crypto_name] = wallet[crypto_name] + share
            else:
                wallet[crypto_name] = share

        month += 1
        if month == 13:
            month = 1
            year += 1

        months_of_investment -= 1
        if months_of_investment == 0:
            break

    # import whole end date table
    data = pd.read_csv('csv/'+str(year)+'_'
                       + '{:02d}'.format(month)
                       + '_coinmarketcap.csv')
    df = pd.DataFrame(data, columns=['name', 'usd'])

    wallet_value = 0

    for name, share in wallet.items():
        rows = df.index[df['name'] == name].tolist()
        coin_value = 0
        if (len(rows) != 0):
            coin_value = float(df.loc[rows[0], 'usd'])
        coin_value_eur = coin_value * share
        wallet_value += coin_value_eur

    growth_factor = wallet_value / invested_usd

    return growth_factor


cryptos_diversification = np.arange(1, max_diversification+1)
# how many months to invest / calculate
months = (end_year - start_year) * 12
months += end_month - start_month
# setup plt
palette = plt.get_cmap('Set1')
color_num = 0


if months < 1:
    print("end of investment is before starting date")
    exit()
else:
    print("timespan of investment: " + str(months) + " months\n")

# calculate growth for each month
while months >= 1:

    print("calculating growth after " + str(months) + " months beginning from "
          + str(start_month) + " " + str(start_year))

    def growth(x): return calculate_growth(start_month, start_year, months, x)
    growth_vectorized = np.vectorize(growth)
    crypto_growth = growth_vectorized(cryptos_diversification)

    plt.plot(crypto_growth, marker='',
             color=palette(color_num),
             linewidth=1,
             alpha=0.9,
             label=months)

    color_num += 1
    months -= 1


plt.legend(loc='upper right', ncol=2, title="months after investment")
plt.title('Growth of Crypto Investments between '
          + str(start_month) + "-" + str(start_year) + " and "
          + str(end_month) + "-" + str(end_year))
plt.xlabel('number of coins invested')
plt.ylabel('growth of investment')
plt.show()
