import requests
import json

class orderManager(self):
    def __init__(self,auth):
        self.auth = auth
        self.url ='https://api.gdax.com'
        
    def renewAuth(self,auth):
        self.auth = auth
    
    def buy(self, **kwargs):
        kwargs["side"] = "buy"
        if "product_id" not in kwargs:
            kwargs["product_id"] = self.product_id
        r = requests.post(self.url + '/orders',
                          data=json.dumps(kwargs),
                          auth=self.auth,
                          timeout=30)
        return r.json()

    def sell(self, **kwargs):
        kwargs["side"] = "sell"
        r = requests.post(self.url + '/orders',
                          data=json.dumps(kwargs),
                          auth=self.auth,
                          timeout=30)
        return r.json()

    def cancel_order(self, order_id):
        r = requests.delete(self.url + '/orders/' + order_id, auth=self.auth, timeout=30)
        return r.json()

    def cancel_all(self, product_id=''):
        url = self.url + '/orders/'
        if product_id:
            url += "?product_id={}&".format(str(product_id))
        r = requests.delete(url, auth=self.auth, timeout=30)
        return r.json()

    def get_order(self, order_id):
        r = requests.get(self.url + '/orders/' + order_id, auth=self.auth, timeout=30)
        return r.json()

    def get_orders(self, product_id=''):
        result = []
        url = self.url + '/orders/'
        if product_id:
            url += "?product_id={}&".format(product_id)
        r = requests.get(url, auth=self.auth, timeout=30)
        return result
