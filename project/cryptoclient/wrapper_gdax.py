
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from cryptoclient.credentials import CredentialsGDAX

credentials = CredentialsGDAX()

API_KEY = credentials.api_key()
# both these need to be in a seperate file later. before you push to github.
API_SECRET = credentials.api_secret()

API_PASS = credentials.api_passphrase()


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
	def __init__(self, api_key, secret_key, passphrase):
		self.api_key = api_key
		self.secret_key = secret_key
		self.passphrase = passphrase

	def __call__(self, request):
		timestamp = str(time.time())
		message = timestamp + request.method + request.path_url + (request.body or b'').decode()
		hmac_key = base64.b64decode(self.secret_key)
		signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
		signature_b64 = base64.b64encode(signature.digest()).decode()

		request.headers.update({
			'CB-ACCESS-SIGN': signature_b64,
			'CB-ACCESS-TIMESTAMP': timestamp,
			'CB-ACCESS-KEY': self.api_key,
			'CB-ACCESS-PASSPHRASE': self.passphrase,
			'Content-Type': 'application/json'
		})
		return request

api_url = 'https://api.gdax.com/'
# auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

# # Get accounts
# r = requests.get(api_url + 'accounts', auth=auth)
# # print r.json()
# # [{"id": "a1b2c3d4", "balance":...

# # Place an order
# order = {
# 	'size': 1.0,
# 	'price': 1.0,
# 	'side': 'buy',
# 	'product_id': 'BTC-USD',
# }
# r = requests.post(api_url + 'orders', json=order, auth=auth)
# # print r.json()
# # {"id": "0428b97b-bec1-429e-a94c-59992926778d"}


class GDAXApi():

	def auth(self):
		auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

		return auth

	def get_accounts(self):
		auth = self.auth()

		r = requests.get(api_url + 'accounts', auth=auth)

		return r.json()

	def create_market_order(self, order_side, order_type, product_id, size):
		auth = self.auth()
		
		order = {
			'type':order_type,
			'size': float(size),
			'side': order_side,
			'product_id': product_id,

		}



		r = requests.post(api_url + 'orders', json=order, auth=auth)

		# print(r.json())

		return r.json()

	def create_limit_order(self, order_side, price, product_id, size, order_type):
		auth = self.auth()

		order = {
			'size': float(size),
			'price':float(price),
			'side': order_side,
			'product_id':product_id,
			'type':order_type
		}

		print(order_side, price, product_id, size, order_type)
		print('CREATE LIMITORDER')
		print(type(order_side), type(price), type(product_id), type(size), type(order_type))
		
		r = requests.post(api_url + 'orders', json=order, auth=auth)

		# print(r.json())

		return r.json()

	def get_crypto_pairs(self):
		auth = self.auth()

		r = requests.get(api_url + 'products', auth=auth)
		# print(r.json(), 'get_crypto_pairs')

		return r.json()

	def get_current_data(self, pair):
		auth = self.auth()

		r = requests.get(api_url + 'products/' + pair + '/ticker', auth=auth)
		# print(r.json())

		return r.json()

	def get_all_open_orders(self):
		auth = self.auth()

		r = requests.get(api_url + 'orders', auth=auth)

		print(r.json())

		return r.json()

	def market_data(self):
		auth = self.auth()

		bitcoin_data = requests.get(api_url + 'products/' + 'BTC-USD' + '/ticker', auth=auth)
		ethereum_data = requests.get(api_url + 'products/' + 'ETH-USD' + '/ticker', auth=auth)
		# print(bitcoin_data.json(), ethereum_data.json(), "1")
		return bitcoin_data.json(), ethereum_data.json()

	def 




























