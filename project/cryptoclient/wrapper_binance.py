import json, hmac, hashlib, time, requests, base64
from cryptoclient.credentials import CredentialsBinance
from requests.auth import AuthBase
import time

time_variable = time.time()

credentials = CredentialsBinance()

api_key = credentials.api_key()


secret_key = credentials.api_secret()

class BinanceApiAuth(AuthBase):
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

api_url = 'https://api.binance.com'

class BinanceAPI():

	def authenticate(self):
		auth = BinanceApiAuth(api_key, secret_key)

		return auth

	def ping(self):
		auth = self.authenticate()

		r = requests.get(api_url + '/api/v1/ping', auth=auth)

		return r.json()

	def get_past_trades(self):
		auth = self.authenticate()

		r = requests.get(api_url + '/api/v1/trades', auth=auth)

		return r.json()

	def ticker(self):
		auth = self.authenticate()

		r = requests.get(api_url + '/api/v3/ticker/price', auth=auth)
		return r.json()

	def old_trades(self, data):
		auth = self.authenticate()

		values = {
			'symbol': data
		}

		r = requests.get(api_url + '/api/v1/historicalTrades', auth=auth)

		return r.json()

	def candlestick_lines(self, data):
		auth = self.authenticate()

		values = {
			'symbol': data,
			'interval': '1d'
		}

		r = requests.get(api_url + '/api/v1/klines', auth=auth)

		return r.json()

	def get_current_open_orders(self):

		auth = self.authenticate()
		print(time.time()* 1000)
		print(type(time.time()))

		values = {
			"timestamp":int(time.time()*1000)
		}

		r = requests.get(api_url + '/api/v3/openOrders', json=values, auth=auth)

		print(r)
		return r.json()

	def delete_order(self, order_id):

		auth = self.authenticate()

		values = {
			'orderId': order_id
		}

		r = requests.delete(api_url + '/api/v3/order', json=values, auth=auth)







