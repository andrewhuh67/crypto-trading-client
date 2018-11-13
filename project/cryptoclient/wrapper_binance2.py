from binance.client import Client
import json, hmac, hashlib, time, requests, base64
from cryptoclient.credentials import CredentialsBinance
from binance.exceptions import BinanceAPIException, BinanceWithdrawException


credentials = CredentialsBinance()

api_key = credentials.api_key()


secret_key = credentials.api_secret()


class Binance2Auth():
	def auth(self):
		client = Client(api_key, secret_key)
		return client

	def get_deposit_address(self, currency):
		auth = self.auth()
		
		address = auth.get_deposit_address(asset=currency)
		return address

	def get_all_tickers(self):
		auth = self.auth()
		prices = auth.get_all_tickers()
		# print(prices)
		return prices
	def every_crypto_binance(self):
		cryptos = ['VET', 'VTHO', 'ENG', 'OST', 'FUN', 'IOTA', 'LEND', 'TNB', 'XLM',
		'POE', 'ICX', 'BNB', 'BTC', 'NEO', 'ETH', 'LTC', 'QTUM', 'EOS', 'SNT', 'BNT',
		 'GAS', 'BCC', 'BTM', 'USDT', 'HCC', 'OAX', 'DNT', 'MCO', 'ICN', 'ZRX', 'OMG',
		  'WTC', 'LRC', 'LLT', 'YOYO', 'TRX', 'STRAT', 'SNGLS', 'KNC', 'BQX', 'SNM',
		   'LINK', 'XVG', 'CTR', 'SALT', 'MDA', 'SUB', 'ETC', 'MTL', 'MTH', 'AST', 'DASH',
		    'BTG', 'EVX', 'REQ', 'VIB', 'POWR','ARK', 'XRP', 'MOD', 'ENJ','STORJ', 'KMD',
		     'RCN', 'NULS', 'RDN', 'XMR', 'DLT', 'AMB', 'BAT', 'ZEC', 'BCPT', 'ARN', 'GVT',
		      'CDT', 'GXS', 'QSP', 'BTS', 'LSK', 'XZC', 'TNT', 'FUEL', 'MANA', 'BCD', 'DGD',
		       'ADX', 'ADA', 'PPT', 'CMT', 'CND', 'WABI', 'SBTC', 'BCX', 'WAVES', 'GTO', 'ELF',
		        'AION', 'NCASH', 'TUSD', 'ATD', 'NEBL', 'BLZ', 'DCR', 'ADD', 'GNT', 'PAX', 'AE',
		         'LOOM', 'KEY', 'HC', 'STEEM', 'GRS', 'EOS', 'ONG', 'WPR', 'NXS', 'DOCK','RLC',
		          'XEM', 'QKC', 'ARDR', 'ZIL', 'THETA', 'LUN', 'DENT', 'POA', 'ZEN', 'REP', 'MFT',
		           'DATA', 'SYS', 'MEETONE', 'BRD', 'VIA', 'RVN', 'BCN', 'NAS', 'CVC', 'GO', 'NANO',
		            'CLOAK', 'NPXS', 'ETF', 'PHX', 'IOST', 'QLC', 'SC', 'POLY', 'INS', 'WAN', 'AGI', 
		            'HOT', 'CHAT', 'STORM', 'IOTX', 'IQ', 'ONT', 'SKY', 'EOP', 'VIBE', 'EDO', 'WINGS',
		             'NAV', 'TRIG', 'APPC', 'PIVX']
		return cryptos

	def create_buymarket_order(self, symbol, quantity, price):

		auth = self.auth()

		# order = auth.order_limit_buy(
	 #    	symbol='BNBBTC',
	 #    	quantity=100,
	 #    	price='0.00001')

		# order = client.order_limit_sell(
  #   		symbol='BNBBTC',
		#     quantity=100,
		#     price='0.00001')

		order = auth.order_market_buy(
		    symbol=symbol,
		    quantity=float(quantity))
		print(price, quantity, symbol)

		# order = auth.order_limit_buy(

		#     symbol=symbol,
		#     quantity=quantity,
		#     price=price)

	def create_buylimit_order(self, symbol, quantity, price):

		auth = self.auth()
		print(type(symbol), type(quantity), type(price),symbol, quantity, price)

		# order = auth.order_limit_buy(
	 #    	symbol='BNBBTC',
	 #    	quantity=100,
	 #    	price='0.00001')

		# order = client.order_limit_sell(
  #   		symbol='BNBBTC',
		#     quantity=100,
		#     price='0.00001')

		order = auth.order_limit_buy(
		    symbol=symbol,
		    quantity=float(quantity),
		    price=price)
		

		# order = auth.order_limit_buy(

		#     symbol=symbol,
		#     quantity=quantity,
		#     price=price)

	def create_sellmarket_order(self, symbol, quantity, price):

		auth = self.auth()

		# order = auth.order_limit_buy(
	 #    	symbol='BNBBTC',
	 #    	quantity=100,
	 #    	price='0.00001')

		# order = client.order_limit_sell(
  #   		symbol='BNBBTC',
		#     quantity=100,
		#     price='0.00001')

		order = auth.order_market_sell(
		    symbol=symbol,
		    quantity=float(quantity),
		    )
		# print(price, quantity, symbol)

		# order = auth.order_limit_buy(

		#     symbol=symbol,
		#     quantity=quantity,
		#     price=price)

	def create_selllimit_order(self, symbol, quantity, price):

		auth = self.auth()

		# order = auth.order_limit_buy(
	 #    	symbol='BNBBTC',
	 #    	quantity=100,
	 #    	price='0.00001')

		# order = client.order_limit_sell(
  #   		symbol='BNBBTC',
		#     quantity=100,
		#     price='0.00001')

		order = auth.order_limit_sell(
		    symbol=symbol,
		    quantity=float(quantity))
		print(price, quantity, symbol)

		# order = auth.order_limit_buy(

		#     symbol=symbol,
		#     quantity=quantity,
		#     price=price)


	def withdraw_binance(self, asset, address, amount):
		
		auth = self.auth()
		try:
    # name parameter will be set to the asset value by the client if not passed
		    result = auth.withdraw(
		        asset=asset,
		        address=address,
		        amount=amount)
		except BinanceAPIException as e:
		    print(e)
		except BinanceWithdrawException as e:
		    print(e)
		else:
		    print("Success")

	def get_open_orders(self):

		auth = self.auth()

		orders = auth.get_open_orders()


		return orders

	def cancel_order(self, orderId, symbol):

		auth = self.auth()

		result = auth.cancel_order(
	    symbol=symbol,
	    orderId=orderId)








