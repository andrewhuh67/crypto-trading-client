import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

from cryptoclient.credentials import CredentialsCoinigy

credentials = CredentialsCoinigy()

api_key = credentials.api_key()


api_secret = credentials.api_secret()


# class ShapeshiftAPI():

# 	def get_coins(self):
# 		r = requests.get(api_url + 'getcoins')

# 		coins = r.json()
# 		return coins

# 	def get_rate(self, pair):
# 		r = requests.get(api_url + 'rate/' + pair)
# 		rate = r.json()

# 		return rate

class CoinigyApiAuth(AuthBase):
	def __init__(self, api_key, secret_key):
		self.api_key = api_key
		self.secret_key = secret_key

	def __call__(self, request):

		request.headers.update(
			{'X-API-KEY': self.api_key, 
				'X-API-SECRET': self.secret_key,
				'Content-Type':'application/json'
			}
		)
		return request

api_url = 'https://api.coinigy.com/api/v1/'

class CoinigyAPI():

	def authenticate(self):

		auth = CoinigyApiAuth(api_key, api_secret)
		
		return auth

	def list_accounts(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'accounts', auth=auth)
		# print(r.json())

		return r.json()

	def list_balances(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'balances', auth=auth)

		# print(r.json())

		return r.json()

	def create_order(self, auth_id, exch_id, mkt_id, order_type_id,price_type_id,limit_price, order_quantity):
		auth = self.authenticate()

		if price_type_id == 'limit':
			price_type_id = str(3)


		values = {
				    "auth_id": int(auth_id),
				    "exch_id": int(exch_id),
				    "mkt_id": int(mkt_id),
				    "order_type_id": int(order_type_id),
				    "price_type_id": price_type_id,
				    "limit_price": float(limit_price),
				    "order_quantity": float(order_quantity)
				  }

		r = requests.post(api_url + 'addOrder', json=values, auth=auth)

		print(auth_id, exch_id, mkt_id, order_type_id, price_type_id, limit_price, order_quantity)
		print(type(auth_id), type(exch_id), type(mkt_id), type(order_type_id), type(price_type_id), type(limit_price), type(order_quantity))
		
		# print(r.json())

		return r.json()



	def get_auth_and_exch_id(self):
		accounts = self.list_accounts()

		accounts = accounts['data'][0]

		# r = requests.post(api_url + 'accounts', auth=auth)

		auth_id = accounts['auth_id']
		exch_id = accounts['exch_id']
		

		return auth_id, exch_id


	def get_mkt_id(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'addOrder', auth=auth)
		pass


	def get_ordertype_pricetype_id(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'OrderTypes', auth=auth)
		# print(r.json())
		return r.json()


	def get_price_type_id(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'addOrder', auth=auth)
		pass

	def list_exchanges(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'exchanges', auth=auth)


		return r.json()

	def list_markets(self, exch_code):
		auth = self.authenticate()

		values = {
			"exchange_code": str("{}".format(exch_code))
		}

		r = requests.post(api_url + 'markets', json=values, auth=auth)


		return r.json()

	def list_orders(self):
		auth = self.authenticate()

		r = requests.post(api_url + 'orders', auth=auth)

		return r.json()

	def list_history_data(self):
		auth = self.authenticate()

		values = {
			"exchange_code": "Binance",
			"exchange_market": 'ETH/ICX',
  			"type": "history"
		}

		r = requests.post(api_url + 'data', json=values, auth=auth)

		return r.json()


	


   

   






	




