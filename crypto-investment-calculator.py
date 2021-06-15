import pandas as pd


###############################################
# info
# this programm will use data in csv/ to simulate a diversificated
# crypto investment. you can setup the timespan, the amount of top
# coins to invest in and how much eur to invest every month.
# the program will display what coins will be in your wallet and
# their value
#
# set your parameters here
#
# when to start investing
start_year = 2018
start_month = 1
# when to stop investing
end_year = 2021
end_month = 1
# total sum of eur split up for all coins
invest_per_month = 100
# amount of coins to buy every month
invested_cryptos = 100
# detailed information
show_investments = False
###############################################


invested_eur = 0
wallet: dict[str, float] = {}

year = start_year
month = start_month


while True:
    if show_investments:
        print("\nCalculating Date: " + str(month) + " " + str(year) + "\n")
    # increase investment
    invested_eur += invest_per_month

    # import selected crypto toplist
    data = pd.read_csv('csv/'+str(year)+'_'
                       + '{:02d}'.format(month)
                       + '_coinmarketcap.csv',
                       nrows=invested_cryptos)
    df = pd.DataFrame(data, columns=['name', 'eur'])

    for i in range(len(df)):
        crypto_name = df.loc[i, 'name']
        crypto_price = float(df.loc[i, 'eur'])
        share = (invest_per_month / invested_cryptos) / crypto_price

        if show_investments:
            print("Buying " + crypto_name.ljust(18)
                  + " at price of " + "{:10.5f}".format(crypto_price).ljust(15)
                  + "\tshare: " "{:10.5f}".format(share))

        if crypto_name in wallet:
            wallet[crypto_name] = wallet[crypto_name] + share
        else:
            wallet[crypto_name] = share

    if (year == end_year) and (month == end_month):
        break

    month += 1
    if month == 13:
        month = 1
        year += 1


# import whole end date table
data = pd.read_csv('csv/'+str(year)+'_'
                   + '{:02d}'.format(month)
                   + '_coinmarketcap.csv')
df = pd.DataFrame(data, columns=['name', 'eur'])

wallet_value = 0.0

print("\nYour Wallet holds:\n")

for name, share in wallet.items():
    rows = df.index[df['name'] == name].tolist()
    coin_value = 0.0
    if (len(rows) != 0):
        coin_value = float(df.loc[rows[0], 'eur'])
    coin_value_eur = coin_value * share
    wallet_value += coin_value_eur
    print("coin: " + name.ljust(18)[:18]
          + " share: " + "{:10.5f}".format(share)
          + "\tvalue in euro: " + "{:10.2f}".format(coin_value_eur))

print("\ntotal eur invested:\t\t" + "{:10.2f}".format(invested_eur))
print("total value in wallet:\t\t" + "{:10.2f}".format(wallet_value))

percentage = wallet_value / invested_eur * 100

print("\ngrowth:\t" + "{:10.2f}".format(percentage) + "%\n")
