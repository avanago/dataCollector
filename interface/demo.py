import json
import requests
import pprint as pp

from coinbaseLinker import coinbaseAccount
from gdax_auth import CoinbaseExchangeAuth
from orderManagement import orderManager


# Step 0
# Initialization

# gdax conf
api_key = 'xxx'
secret_key = 'xxx'
passphrase = 'xxx'

# coinbase conf
coinbase_account_id = 'xxx'

auth  = CoinbaseExchangeAuth(api_key, secret_key, passphrase)
coinbase =coinbaseAccount(auth, coinbase_account_id)
order = orderManager(auth)


# Step 1
# take credits from coinbase
coinbaseResponse = coinbase.depositFromCoinbase(amount = 100, currency='BTC'):
pp.pprint(coinbaseResponse)
    
# Step 2
# place a buy order, limit type
createOrder = { "size": "0.01",
                "price": "0.100",
                "side": "buy",
                "product_id": "BTC-USD",
                "type":'limit'
               }
createOrderResponse = order.buy(createOrder)
order_id = createOrderResponse['id']
pp.pprint(createOrderResponse)


# Step 3
# check the order
getOrderResponse = order.get_order(order_id)
pp.pprint(getOrderResponse)


# Step 4
# delete single order
cancelOrderResponse = order.cancel_order(order_id)
pp.pprint(cancelOrderResponse)


# Step 5
# place sell order
createOrder = { "size": "0.01",
                "price": "10000000000",
                "side": "sell",
                "product_id": "BTC-USD",
                "type":'limit'
               }

createOrderResponse = order.sell(createOrder)
order_id = createOrderResponse['id']
pp.pprint(createOrderResponse)


# Step 6
# verify the sell order
getOrderResponse = order.get_order(order_id)
pp.pprint(getOrderResponse)


# Step 7
# delete order
getCancelResponse = order.cancel_order(order_id)
pp.pprint(getCancelResponse)


# Step 8
# place 7 order 

createOrder = { "size": "0.01",
                "price": "60000",
                "side": "sell",
                "product_id": "BTC-USD",
                "type":'limit'
               }

for i in range(7):
    createOrderResponse = order.sell(createOrder)
    order_id = createOrderResponse['id']
    pp.pprint(createOrderResponse)

    
# Step 9
# Verify all the order
responseGetOrders = order.get_orders()
pp.pprint(responseGetOrders)


# Step 10
# Cancel all orders
responseCanc = order.cancel_all()
pp.pprint(responseCanc)


# Step 11
# take credits back to coinbase
coinbaseResponse = coinbase.withdrawToCoinbase(amount=100, currency="BTC")
pp.pprint(coinbaseResponse)

