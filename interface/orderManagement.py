import requests
import json

class orderManager(self):
    def __init__(self, auth, prodTrader=False):
        self.auth = auth
        if prodTrader:
            self._url = 'https://api.gdax.com'
        else:
            self._url = 'https://api-public.sandbox.gdax.com'
        
    def renewAuth(self,auth):
        self.auth = auth
    
    def buy(self, **kwargs):
        kwargs["side"] = "buy"
        r = requests.post(self._url + '/orders',
                          data=json.dumps(kwargs),
                          auth=self.auth,
                          timeout=30)
        return r.json()

    def sell(self, **kwargs):
        kwargs["side"] = "sell"
        r = requests.post(self._url + '/orders',
                          data=json.dumps(kwargs),
                          auth=self.auth,
                          timeout=30)
        return r.json()

    def cancel_order(self, order_id):
        r = requests.delete(self._url + '/orders/' + order_id, auth=self.auth, timeout=30)
        return r.json()

    def cancel_all(self, product_id=''):
        _url = self._url + '/orders/'
        if product_id:
            _url += "?product_id={}&".format(str(product_id))
        r = requests.delete(_url, auth=self.auth, timeout=30)
        return r.json()

    def get_order(self, order_id):
        r = requests.get(self._url + '/orders/' + order_id, auth=self.auth, timeout=30)
        return r.json()

    def get_orders(self, product_id=''):
        result = []
        _url = self._url + '/orders/'
        if product_id:
            _url += "?product_id={}&".format(product_id)
        r = requests.get(_url, auth=self.auth, timeout=30)
        return result
