

class coinbaseAccount(self)
  def __init__(self):

  def coinbase_deposit(self, amount="", currency="", coinbase_account_id=""):
    payload = {
        "amount": amount,
        "currency": currency,
        "coinbase_account_id": coinbase_account_id
    }
    r = requests.post(self.url + "/deposits/coinbase-account", data=json.dumps(payload), auth=self.auth, timeout=30)
    # r.raise_for_status()
    return r.json()

  def coinbase_withdraw(self, amount="", currency="", coinbase_account_id=""):
    payload = {
        "amount": amount,
        "currency": currency,
        "coinbase_account_id": coinbase_account_id
    }
    r = requests.post(self.url + "/withdrawals/coinbase-account", data=json.dumps(payload), auth=self.auth, timeout=30)
    # r.raise_for_status()
    return r.json()
