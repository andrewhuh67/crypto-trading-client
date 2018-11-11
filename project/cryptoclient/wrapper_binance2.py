from binance.client import Client
import json, hmac, hashlib, time, requests, base64
from cryptoclient.credentials import CredentialsCoinigy


credentials = CredentialsCoinigy()

api_key = credentials.api_key()


secret_key = credentials.api_secret()


class Binance2Auth():
	def auth(self):
		client = Client(api_key, secret_key)
		return client

	def get_deposit_address(self, currency):
		auth = self.auth()
		address = auth.get_deposit_address(currency)
		return address

	def get_all_tickers(self):
		auth = self.auth()
		prices = auth.get_all_tickers()
		# print(prices)
		return prices
	def every_crypto_binance(self):
		cryptos = ['VET', 'VTHO', 'ENG', 'OST', 'FUN', 'IOTA', 'LEND', 'TNB', 'XLM',
		'POE', 'ICX', 'BNB', 'BTC', 'NEO', 'ETH', 'LTC', 'QTUM', 'EOS']