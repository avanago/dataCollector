# Credits goes to https://github.com/danpaquin/gdax-python
#
# Refactor and rearrangement of the gdax-python
#
# this file creates a class able to connect to collect data from gdax

# TO DO: divide in two subclasses - snapshotter and follower

import json
from websocket import create_connection, WebSocketConnectionClosedException
from gdax.public_client import PublicClient
from bintrees import RBTree
from decimal import Decimal
import requests


class obook(object):

    def __init__(self,saveMessage = 0,product_id = 'BTC-USD'):

        self.url = "wss://ws-feed.gdax.com/"
        self.ws = create_connection(self.url)
        self.product_id = product_id
        self.sequence = -1
        self.stop = False
        self._sequence = -1
        self._client = PublicClient()
        self._asks = RBTree()
        self._bids = RBTree()
        self._current_ticker = None
        self.saveMessage = saveMessage
        self.t1 = None
        self.t2 = None
        self.t3 = None
        
    def saveMessage(self,msg):
        ### To be done - save live message in file
        path = 'xxx'
        with open (pathOUT,'a') as fileIO:
            pathOUT.write(json.dumps(msg))
        a=4
        
    def demo(self):
        self.connect()
        self.listen(demo=1)
        self.disconnect()        
        
    def connect(self):
        print('connessione')
        sub_params = {'type': 'subscribe', 'product_ids': [product_id]}
        self.ws.send(json.dumps(sub_params))
        sub_params = {"type": "heartbeat", "on": False}
        self.ws.send(json.dumps(sub_params))
        c= 0
    
    def listen(self,demo=0):
        print('in ascolto')
        count = 0
        while not self.stop:
            data = self.ws.recv()
            msg = json.loads(data)
            self.onmessage(msg)
            print msg['sequence']
            count = count + 1
            if count>10 and demo:
                self.stop = True
    
    def disconnect(self):
        print('Fine Connessione')
        #self.reset_book()
        
       
    def get_snapshot(self):
        self.reset_book()
        
    def reset_book(self):
        self._asks = RBTree()
        self._bids = RBTree()
        self.tref = datetime.datetime.now()
        # res = self._client.get_product_order_book(product_id=self.product_id, level=3)
        ##################
        params = {'level': 3}
        r = requests.get('https://api.gdax.com/products/{}/book'
                         .format(self.product_id), params=params, timeout=30)
        try:
            res = r.json()
        except:
            res['bids'] = {}
            res['asks'] = {}
            res['sequence'] = 0
        # r.raise_for_status()

        
        ##################
        for bid in res['bids']:
            self.add1({
                'id': bid[2],
                'side': 'buy',
                'price': Decimal(bid[0]),
                'size': Decimal(bid[1])
            })
        for ask in res['asks']:
            self.add1({
                'id': ask[2],
                'side': 'sell',
                'price': Decimal(ask[0]),
                'size': Decimal(ask[1])
            })
        self._sequence = res['sequence']
        
    def onmessage(self,msg):
        if self.saveMessage:
            saveMessage(msg)
        message = msg
        sequence = message['sequence']
        if self._sequence == -1:
            self.reset_book()
            return
        if sequence <= self._sequence:
            # ignore older messages (e.g. before order book initialization from getProductOrderBook)
            return
        elif sequence > self._sequence + 1:
            self.on_sequence_gap(self._sequence, sequence)
            return
        
        msg_type = message['type']
        if msg_type == 'open':
            self.add(message)
        elif msg_type == 'done' and 'price' in message:
            self.remove(message)
        elif msg_type == 'match':
            self.match(message)
            self._current_ticker = message
        elif msg_type == 'change':
            self.change(message)        


    def get_current_book_serializable(self):
        result = {
            'sequence': self._sequence,
            'asks': [],
            'bids': [],
        }
        for ask in self._asks:
            try:
                # There can be a race condition here, where a price point is removed
                # between these two ops
                this_ask = self._asks[ask]
            except KeyError:
                continue
            for order in this_ask:
                result['asks'].append([float(order['price']), float(order['size']), order['id']])
        for bid in self._bids:
            try:
                # There can be a race condition here, where a price point is removed
                # between these two ops
                this_bid = self._bids[bid]
            except KeyError:
                continue

            for order in this_bid:
                result['bids'].append([float(order['price']), float(order['size']), order['id']])
        return result

            
            
    def get_current_book(self):
        result = {
            'sequence': self._sequence,
            'asks': [],
            'bids': [],
        }
        for ask in self._asks:
            try:
                # There can be a race condition here, where a price point is removed
                # between these two ops
                this_ask = self._asks[ask]
            except KeyError:
                continue
            for order in this_ask:
                result['asks'].append([order['price'], order['size'], order['id']])
        for bid in self._bids:
            try:
                # There can be a race condition here, where a price point is removed
                # between these two ops
                this_bid = self._bids[bid]
            except KeyError:
                continue

            for order in this_bid:
                result['bids'].append([order['price'], order['size'], order['id']])
        return result
    
    def on_sequence_gap(self, gap_start, gap_end):
        self.reset_book()
        print('Error: messages missing ({} - {}). Re-initializing  book at sequence.'.format(
            gap_start, gap_end, self._sequence))
        
        
    #### UTILS

    def remove(self, order):
        price = Decimal(order['price'])
        if order['side'] == 'buy':
            bids = self.get_bids(price)
            if bids is not None:
                bids = [o for o in bids if o['id'] != order['order_id']]
                if len(bids) > 0:
                    self.set_bids(price, bids)
                else:
                    self.remove_bids(price)
        else:
            asks = self.get_asks(price)
            if asks is not None:
                asks = [o for o in asks if o['id'] != order['order_id']]
                if len(asks) > 0:
                    self.set_asks(price, asks)
                else:
                    self.remove_asks(price)

    def match(self, order):
        size = Decimal(order['size'])
        price = Decimal(order['price'])

        if order['side'] == 'buy':
            bids = self.get_bids(price)
            if not bids:
                return
            assert bids[0]['id'] == order['maker_order_id']
            if bids[0]['size'] == size:
                self.set_bids(price, bids[1:])
            else:
                bids[0]['size'] -= size
                self.set_bids(price, bids)
        else:
            asks = self.get_asks(price)
            if not asks:
                return
            assert asks[0]['id'] == order['maker_order_id']
            if asks[0]['size'] == size:
                self.set_asks(price, asks[1:])
            else:
                asks[0]['size'] -= size
                self.set_asks(price, asks)

    def change(self, order):
        try:
            new_size = Decimal(order['new_size'])
        except KeyError:
            return

        try:
            price = Decimal(order['price'])
        except KeyError:
            return

        if order['side'] == 'buy':
            bids = self.get_bids(price)
            if bids is None or not any(o['id'] == order['order_id'] for o in bids):
                return
            index = [b['id'] for b in bids].index(order['order_id'])
            bids[index]['size'] = new_size
            self.set_bids(price, bids)
        else:
            asks = self.get_asks(price)
            if asks is None or not any(o['id'] == order['order_id'] for o in asks):
                return
            index = [a['id'] for a in asks].index(order['order_id'])
            asks[index]['size'] = new_size
            self.set_asks(price, asks)

        tree = self._asks if order['side'] == 'sell' else self._bids
        node = tree.get(price)

        if node is None or not any(o['id'] == order['order_id'] for o in node):
            return

    def get_current_ticker(self):
        return self._current_ticker
    
########################################    
    def add1(self, order):
        order = {
            'id': order.get('order_id') or order['id'],
            'side': order['side'],
            'price': float(order['price']),
            'size': float(order.get('size') or order['remaining_size'])
        }
        if order['side'] == 'buy':
            bids = self.get_bids(order['price'])
            if bids is None:
                bids = [order]
            else:
                bids.append(order)
            self.set_bids(order['price'], bids)
        else:
            asks = self.get_asks(order['price'])
            if asks is None:
                asks = [order]
            else:
                asks.append(order)
            self.set_asks(order['price'], asks)      
########################################    
    
    def add(self, order):
        order = {
            'id': order.get('order_id') or order['id'],
            'side': order['side'],
            'price': Decimal(order['price']),
            'size': Decimal(order.get('size') or order['remaining_size'])
        }
        if order['side'] == 'buy':
            bids = self.get_bids(order['price'])
            if bids is None:
                bids = [order]
            else:
                bids.append(order)
            self.set_bids(order['price'], bids)
        else:
            asks = self.get_asks(order['price'])
            if asks is None:
                asks = [order]
            else:
                asks.append(order)
            self.set_asks(order['price'], asks)        

    def get_bids(self, price):
        return self._bids.get(price)
    
    def set_bids(self, price, bids):
        self._bids.insert(price, bids)

    def get_asks(self, price):
        return self._asks.get(price)    
    
    def set_asks(self, price, asks):
        self._asks.insert(price, asks)    
        
        
if __name__ == "__main__":
    import time



    import json

    import time
    import datetime

    print('Start gdax collection...')

    outFolder = '/home/andre/tmp/'
    ob_btc = obook(product_id = 'BTC-USD')
    ob_eth = obook(product_id = 'ETH-USD')
    ob_ltc = obook(product_id = 'LTC-USD')

    booklive = dict()
    sleepTime = 4

    print ('Initialization Complete...')
    while 1:
        
        timeStamp = datetime.datetime.now()

        
        print('Start Iteration... '+ str(datetime.datetime.now()))
        
        ob_btc.get_snapshot()
        booklive['BTC-USD'] = ob_btc.get_current_book_serializable()
        booklive['BTC-USD']['Tref'] = ob_btc.tref.strftime('%s')
        print('BTC-USD complete')
        
        ob_eth.get_snapshot()
        booklive['ETH-USD'] = ob_eth.get_current_book_serializable()
        booklive['ETH-USD']['Tref'] = ob_eth.tref.strftime('%s')
        print('ETH-USD complete')
        
        ob_ltc.get_snapshot()
        booklive['LTC-USD'] = ob_ltc.get_current_book_serializable()
        booklive['LTC-USD']['Tref'] = ob_ltc.tref.strftime('%s')
        print('LTC-USD complete')
        
        Fname = timeStamp.strftime('%Y%m%d')
        pathM = outFolder + Fname + '_gdaxSampler.json'

        with open (pathM,'a') as fileIO:
            fileIO.write(json.dumps(booklive))    

        print('End Iteration... '+ str(datetime.datetime.now()))
        time.sleep(10*60)
        
