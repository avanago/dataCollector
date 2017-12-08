import json
import requests

class coinbaseAccount():
    def __init__(self, auth, coinbase_account_id, prodTrader=False):
        self.coinbase_account_id = coinbase_account_id
        self.auth = auth
        if prodTrader:
            self._url = 'https://api.gdax.com'
        else:
            self._url = 'https://api-public.sandbox.gdax.com'

    def depositFromCoinbase(self, amount = 0, currency=""):
        payload = {
            "amount": amount,
            "currency": currency,
            "coinbase_account_id": self.coinbase_account_id
        }
        r = requests.post(self._url + "/deposits/coinbase-account", data=json.dumps(payload), auth=self.auth, timeout=30)
        return r.json()

    def withdrawToCoinbase(self, amount=0, currency=""):
        payload = {
            "amount": amount,
            "currency": currency,
            "coinbase_account_id": self.coinbase_account_id
        }
        r = requests.post(self._url + "/withdrawals/coinbase-account", data=json.dumps(payload), auth=self.auth, timeout=30)
        return r.json()
      
