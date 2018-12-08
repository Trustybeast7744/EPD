from binance.client import Client
import time
import csv

api_secret = "NQTneKrJXluHCcmU5LkHX7Uk9qKJvuOB37ilHNt4nyeXll9harecCncLwgM24Q63"
api_key = "ezynC6e1QBhbQYP9sM0pvLjb3VRyASAE9VFF808MIBzyfdKnOw8AWrnPCWq8p1wL"

client = Client(api_key, api_secret)


q = client.get_recent_trades(symbol="ETHUSDT")

buys = []
sells = []
buys_disc = []
sells_disc = []
a_eth_buy = []
a_eth_sell = []
price_over_time = []


def buy(prc, qty):
    USD_amount_b = prc * qty
    if USD_amount_b >= 0:
        print("BUY: ${}, PRICE: ${}, qty: {} ETH".format(USD_amount_b, prc, qty))
        buys_disc.append(["BUY:", USD_amount_b])
        buys.append(USD_amount_b)
        a_eth_buy.append(qty)
        return


def sell(prc, qty):
    USD_amount_s = prc * qty
    if USD_amount_s >= 0:
        print("SELL: ${}, PRICE: ${}, qty: {} ETH".format(USD_amount_s, prc, qty))
        sells_disc.append(["SELL:", USD_amount_s])
        sells.append(USD_amount_s)
        a_eth_sell.append(qty)
        return


t_end = time.time() + 60 * (1/4)
while time.time() < t_end:
    trades = client.get_recent_trades(symbol="ETHUSDT")
    price = float(trades[-1]['price'])
    amount = float(trades[-1]['qty'])
    is_sell = trades[-1]['isBuyerMaker']
    price_over_time.append(price)
    if is_sell:
        sell(price, amount)
    elif not is_sell:
        buy(price, amount)


buys = list(set(buys))
sells = list(set(sells))
price_over_time = list(set(price_over_time))
a_eth_buy = list(set(a_eth_buy))
a_eth_sell = list(set(a_eth_sell))


def get_volume_USD(l):
    new_l = []
    c_sum = 0
    for elt in l:
        c_sum += elt
        new_l.append(c_sum)
    return new_l


def to_csv(data, name):
    with open("{}.csv".format(name), "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(("{}".format(name), ""))
        for val in data:
            writer.writerow([val])


volumes_buy = get_volume_USD(buys)
volumes_sell = get_volume_USD(sells)
volumes_eth_buy = get_volume_USD(a_eth_buy)
volumes__eth_sell = get_volume_USD(a_eth_sell)

to_csv(buys, "Buy (USD)")
to_csv(sells, "Sell (USD)")
to_csv(volumes_buy, "Volume USD (Buy)")
to_csv(volumes_sell, "Volume USD (Sell)")
to_csv(volumes_eth_buy, "Volume ETH (Buy)")
to_csv(volumes__eth_sell, "Volume ETH (Sell)")
to_csv(price_over_time, "Price (USD)")


print("")

print("Buys $ Amount: ${}".format(sum(buys)))
print("Sells $ Amount: ${}".format(sum(sells)))
print("Number of SELLS above or equal to 1000: {}".format(len(sells)))
print("Number of BUYS above or equal to 1000: {}".format(len(buys)))
print("Initial Price: ${}, Final Price ${}".format(price_over_time[0], price_over_time[-1]))

print("")

print("Biggest Buy $ Order: ${}".format(max(buys)))
print("Biggest Sell $ Order: ${}".format(max(sells)))

