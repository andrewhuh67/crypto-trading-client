from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.views.generic import View
from datetime import date
import time
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
from matplotlib import style
import numpy as np
from cryptoclient.wrapper_coinbase import Wallet
from cryptoclient.wrapper_gdax import GDAXApi
from cryptoclient.wrapper_coinigy import CoinigyAPI
from cryptoclient.wrapper_binance import BinanceAPI
from cryptoclient.wrapper_binance2 import Binance2Auth
from cryptoclient.models import UserAddresses, UserCredentials

from cryptoclient.form import WalletCreationForm, LimitOrderForm, CryptoToCryptoForm, WalletSendMoneyForm, BetweenGDAXAndCBForm, ChartForm, SwapCryptoSendMoneyForm, DeleteOrderForm, SubmitKeysForm

# Create your views here.

class OptionListView(View):
	
	def get(self, request):
		GDAX = GDAXApi()
		bitcoin_data, ethereum_data = GDAX.market_data()

		context = {
			'bitcoin_data':bitcoin_data,
			'ethereum_data':ethereum_data
		}
		return render(request, 'cryptoclient/option.html', context)

class SubmitKeyView(View):

	form_class = SubmitKeysForm

	def get(self, request):

		form = self.form_class()


		print(request.user.id, "user_id")

		context = {
			'form':form
		}

		return render(request, 'cryptoclient/submit-keys.html', context)

	def post(self, request):

		print("this is before the request")

		user = User.objects.get(id=request.user.id)

		# current_user = get_user_model()
		# print(current_user)
		
		form = self.form_class(request.POST)

		# user = get_object_or_404(User, pk=request.user.id)
		print(user)
		# form1 = self.form_class()
		# print(request.POST, "request")

		# print("right before form")
		

		
		if form.is_valid():

			cb_api_key = request.POST['cb_api_key']
			cb_secret_key = request.POST['cb_secret_key'] 
			gdax_api_key = request.POST['gdax_api_key']
			gdax_secret_key = request.POST['gdax_secret_key']
			gdax_passphrase = request.POST['gdax_passphrase']
			coinigy_api_key = request.POST['coinigy_api_key']
			coinigy_api_secret = request.POST['coinigy_api_secret']
			binance_api_key = request.POST['binance_api_key']
			binance_api_secret = request.POST['binance_api_secret']

			user_cred = UserCredentials()

			user_cred.cb_api_key = request.POST['cb_api_key']
			user_cred.cb_secret_key = request.POST['cb_secret_key']
			user_cred.gdax_api_key = request.POST['gdax_api_key']
			user_cred.gdax_secret_key = request.POST['gdax_secret_key']
			user_cred.gdax_passphrase = request.POST['gdax_passphrase']
			user_cred.coinigy_api_key = request.POST['coinigy_api_key']
			user_cred.coinigy_api_secret = request.POST['coinigy_api_secret']
			user_cred.binance_api_key = request.POST['binance_api_key']
			user_cred.binance_api_secret = request.POST['binance_api_secret']
			user_cred.user = user
			user_cred.save()
			print("WEWEWEWEWEWEWE")

			return redirect('cryptoclient:options-list')
		
		else:
			
			context = {
				'form':form1
			}

			return render(request, 'cryptoclient/submit-keys.html', context)




class WalletListView(View):

	def get(self, request):

		auth = Wallet()

		accounts = auth.get_accounts()
		print(accounts)

		
		list_wallets = auth.list_wallets()

		context = {
			"wallets": list_wallets['data']
		}
		return render(request, 'cryptoclient/wallet-list.html', context)

class WalletCreateView(View):

	form_class = WalletCreationForm
	template_name = 'cryptoclient/wallet-create.html'
	success_url = 'cryptoclient:wallet-list'


	def get(self, request):
		walletcreationform = self.form_class()
		context = {
			"form": walletcreationform
		} 
		
		return render(request, self.template_name, context)

	def post(self, request):
		walletcreationform = self.form_class(request.POST)
		
		if walletcreationform.is_valid():
			name = request.POST["name"]
			
			auth = Wallet()
			address = auth.create_wallet(name)
			return redirect(self.success_url)

		else:	
			return render(request, self.template_name, {'form': walletcreationform})

class WalletAddressView(View):

	template_name = 'cryptoclient/wallet-addresses.html'

	def get(self, request):
		auth = Wallet()

		
		list_wallets = auth.list_wallets()
		list_wallets = list_wallets['data']
		# print(list_wallets, "list_wallets")
		
		# print(list_wallets)

		list_address = auth.get_addresses()
		# print(list_address)
		
		context = {
			"addresses": list_address,
			"wallets": list_wallets
		}

		return render(request, self.template_name, context)

	def post(self, request):
		pass

# need a new name for this view
class WalletTransactionView(View):
	template_name = 'cryptoclient/wallet-send-money.html'
	form_class = WalletSendMoneyForm

	def get(self, request):
		transaction_form = self.form_class()

		
		context = {
			'form':transaction_form
		}

		return render(request, self.template_name, context)

	def post(self, request):
		auth = Wallet()
		gdax = GDAXApi()
		
		data = request.POST

		wallettransactionform = self.form_class(request.POST)

		list_wallets = auth.list_wallets()
		list_wallets = list_wallets['data']
		print(list_wallets)

		print(data)
		if data['currency'] == "1":
			crypto = 'BTC'
		elif data['currency'] == "2":
			crypto = 'ETH'
		elif data['currency'] == "3":
			crypto = 'BCH'
		elif data['currency'] == "4":
			crypto = 'LTC'

		for wallet in list_wallets:
			if wallet['currency'] == crypto:
				account_id = wallet['id']

		if wallettransactionform.is_valid():
			address = data['to_address']
			amount = data['amount']
			print(address, amount)
			auth.send_money(address,amount,crypto, account_id)
			
			
			# print(send_money)

			return redirect('cryptoclient:wallet-list')

		else:
			return render(request, self.template_name, {'form': wallettransactionform})

class WalletCoinbaseGDAXTransferView(View):

	template_name = 'cryptoclient/wallet-transaction-gdax.html'
	form_class = BetweenGDAXAndCBForm

	def get(self, request):
		GDAX = GDAXApi()
		# accounts = GDAX.get_accounts()
		# print(accounts)
		auth = Wallet()

		accounts = auth.get_accounts()
		print(accounts['data'])

		transfer_form = self.form_class()
		
		context = {
			'form':transfer_form
		}

		return render(request, self.template_name, context)

	def post(self, request):


		auth = Wallet()

		accounts = auth.get_accounts()
		print(accounts)

		GDAX = GDAXApi()
		data = request.POST
		# print(request.POST)
		cb_accounts = GDAX.list_cb_accounts()
		print(cb_accounts, "hererere")
		transfer_form = self.form_class(request.POST)

		# get coinbase accounts
		# match the accounts with the currency they chose

		coinbase_account_id = request.POST['currency']
		if coinbase_account_id == "1":
			coinbase_account_id = "BTC"
		elif coinbase_account_id == "2":
			coinbase_account_id = "ETH"
		elif coinbase_account_id == "3":
			coinbase_account_id = "BCH"
		elif coinbase_account_id == "4":
			coinbase_account_id = "LTC"  

		# accounts = GDAX.get_accounts()
		# print(accounts)
		for account in accounts['data']:
			print(account['currency'])
			if coinbase_account_id == account['currency']:
				print(coinbase_account_id)
				coinbase_account_id = account['id']
				print(coinbase_account_id)



		if transfer_form.is_valid():
			amount = request.POST['amount']
			amount = float(amount)
			currency = request.POST['currency']
			if currency == "1":
				currency = "BTC"
			elif currency == "2":
				currency = "ETH"
			elif currency == "3":
				currency = "BCH"
			elif currency == "4":
				currency = "LTC"
			print(currency, "currency")
			transaction_type = request.POST['transaction']

			if transaction_type == "1":
				GDAX.withdraw_to_coinbase(amount, currency, coinbase_account_id)
				print("got here")
			elif transaction_type == "2":
				GDAX.deposit_to_gdax(amount, currency, coinbase_account_id)

			return redirect('cryptoclient:wallet-list')

		else:
			return HttpResponse("Your form is broken")


class BuySellView(View):

	form_class = LimitOrderForm

	def get(self, request):
		purchaseorderform = self.form_class()
		GDAX = GDAXApi()

		accounts = GDAX.get_accounts()
		crypto_pairs = GDAX.get_crypto_pairs()
		crypto_price = GDAX.get_current_data('BTC-USD')
		# print(crypto_price)
		# print("XOXOXOXOXOXOXOOXOXOXOXOXO")

		all_open_orders = GDAX.get_all_open_orders()

		binance = BinanceAPI()

		ping = binance.ping()

		print(ping, "yesornowes")



		

		context = {
			'accounts':accounts,
			'form':purchaseorderform,
			'crypto_pairs':crypto_pairs,
			'open_orders':all_open_orders,
			# 'LTC_close_data':json.dumps(LTC_close_data)	
		}

		return render(request, 'cryptoclient/buy-sell.html', context)


	def post(self, request):
		purchaseorderform = self.form_class(request.POST)

		GDAX = GDAXApi()
		test = type(request.POST['order_type'])
		print(test)
		another_str = int(request.POST['order_type'])
		print(another_str)
		print(request.POST)

		if request.POST['order_type'] == "1":
			order_type = 'market'
		elif request.POST['order_type'] == "2":
			order_type = 'limit'

		if request.POST['order_side'] == "1":
			order_side = 'buy'
		elif request.POST['order_side'] == "2":
			order_side = 'sell'

		if request.POST['crypto_pair'] == "1":
			crypto_pair = 'BTC-USD'
		elif request.POST['crypto_pair'] == "2":
			crypto_pair = 'ETH-USD'
		elif request.POST['crypto_pair'] == "3":
			crypto_pair = 'BCH-USD'
		elif request.POST['crypto_pair'] == "4":
			crypto_pair = 'LTC-USD'

		price = request.POST['price']
		amount = request.POST['amount']
		print(order_type, order_side, crypto_pair, price, amount, "POST")

		print(order_type,"type", order_side,"buyorsell")



		if purchaseorderform.is_valid():
			
			if order_type == "limit":
				order = GDAX.create_limit_order(order_side, price, crypto_pair, amount, order_type)
				print(order, "limit")

			elif order_type == "market":
				order = GDAX.create_market_order(order_side, price, crypto_pair, amount, order_type)
				print(order, "market")

			return redirect('cryptoclient:options-list')

		else:
			print('form is broken')
			return redirect('cryptoclient:buy-sell')

class BuySellDataView(View):

	def get(self, request):

		GDAX = GDAXApi()


		start = date(2017, 12, 4).isoformat()
		end = date(2018, 7, 3).isoformat()
		# print(start, end)
		# style.use('ggplot')
		granularity = '86400'
		BTC_candle_data = GDAX.get_candle_data(start, end, granularity, 'BTC-USD')
		# ETH_candle_data = GDAX.get_candle_data(start, end, granularity, 'ETH-USD')
		# LTC_candle_data = GDAX.get_candle_data(start, end, granularity, 'LTC-USD')
		# print(ETH_candle_data)
		# print(BTC_candle_data)
		BTC_close_data = GDAX.get_close_data(BTC_candle_data)
		# ETH_close_data = GDAX.get_close_data(ETH_candle_data)
		# LTC_close_data = GDAX.get_close_data(LTC_candle_data)
		# print(LTC_candle_data)

		# ltc_json = GDAX.to_json(LTC_close_data)
		# print(ETH_close_data)

		# GDAX.to_csv(BTC_close_data, 'BTC-USD')
		# GDAX.to_csv(ETH_close_data, 'ETH-USD')
		# GDAX.to_csv(LTC_close_data, 'LTC-USD')

		# url(r'^crypto/buy-sell/data$', views.BuySellDataView.as_view(), name="buy-sell-data"),
		# print(ltc_json)
		crypto_json = {}
		BTC_close_data.insert(0, 'BTC')
		# ETH_close_data.insert(0, 'ETH')
		# LTC_close_data.insert(0, 'LTC')
		# print(LTC_close_data)
		# crypto_json['LTC'] = LTC_close_data
		crypto_json['BTC'] = BTC_close_data
		# crypto_json['ETH'] = ETH_close_data

		
		# print(ltc_json)
		print(crypto_json, "wow")
		return JsonResponse(crypto_json)

class BuySellOrderView(View):

	form_class = DeleteOrderForm

	def get(self,request):
		GDAX = GDAXApi()

		form = self.form_class()

		all_open_orders = GDAX.get_all_open_orders()


		# if price > crypto_price['price']:
		# 	stop = 'loss'

		# elif price < crypto_price['price']:
		# 	stop = 'entry'
		# order = GDAX.create_order()

		context = {
			'form':form,
			'open_orders':all_open_orders
		}

		return render(request, 'cryptoclient/buy-sell-order.html', context)

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			order_id = request.POST['orderId']
			symbol = request.POST['symbol']

			GDAX = GDAXApi()
			GDAX.cancel_order(order_id)

			return redirect('cryptoclient:buy-sell-order')

		else:
			return HttpResponse('Didnt Work')


class BuySellAccountsView(View):

	def get(self,request):
		GDAX = GDAXApi()

		

		accounts = GDAX.get_accounts()


		# if price > crypto_price['price']:
		# 	stop = 'loss'

		# elif price < crypto_price['price']:
		# 	stop = 'entry'
		# order = GDAX.create_order()

		# print(accounts)

		account_info = {}

		for account in accounts:
			if account["currency"] == "USD":
				continue
			account_info[str(account["currency"])] = account["id"]

		print(account_info, "account_info")

		# now get the account address



		context = {
			
			'accounts':accounts
		}
		

		return render(request, 'cryptoclient/buy-sell-accounts.html', context)



class ProfileView(View):

	def get(self, request):

		# list_of_all_ids = [litecoin_id, bitcoin_id, bitcoin_cash_id, ethereum_id, usd_id]
		# list_of_all_binance_pairs = ['BCC/BTC', 'BTC/USDT', 'BCC/USDT', ]

		list_of_all_pastbuysell_transactions = []
		auth = Wallet()

		binance = BinanceAPI()
		binance_data = binance.get_past_trades()
		ticker_data = binance.ticker()
		print(ticker_data, "thisthisthisthis")
		ticker_list = []

		for ticker in ticker_data:
			ticker_list.append(ticker['symbol'])
		# print(ticker_list)

		# for ticker in ticker_list:
		# 	trades = binance.old_trades(ticker)
			# print(trades)



		# these are just the pastbuysell

		# all_transactions = auth.get_all_transactions()

		

		all_accounts = auth.get_accounts()
		# print(all_accounts, "all accounts")
		litecoin_id = all_accounts['data'][2]['id']
		bitcoin_id = all_accounts['data'][4]['id']
		bitcoin_cash_id = all_accounts['data'][0]['id']
		ethereum_id = all_accounts['data'][3]['id']
		usd_id = all_accounts['data'][1]['id']

		list_of_all_ids = [litecoin_id, bitcoin_id, bitcoin_cash_id, ethereum_id, usd_id]

		for crypto_id in list_of_all_ids:
			transactions = auth.get_all_transactions(crypto_id)

			number_of_transaction = len(transactions['data'])

			for transaction in range(0, number_of_transaction-1):
				# print(transactions['data'], "RIGHT HERE")
				list_of_all_pastbuysell_transactions.append(transactions['data'][transaction])



		# print(list_of_all_pastbuysell_transactions, "alltransaction")

		newlist = sorted(list_of_all_pastbuysell_transactions, key=lambda k: k['created_at'], reverse=True) 

		# print(newlist, "right here")


		litecoin_transactions = auth.get_all_transactions(litecoin_id)
		bitcoin_transactions = auth.get_all_transactions(bitcoin_id)
		bitcoin_cash_transactions = auth.get_all_transactions(bitcoin_cash_id)
		ethereum_transactions = auth.get_all_transactions(ethereum_id)
		usd_transactions = auth.get_all_transactions(usd_id)
		# print(litecoin_transactions['data'], "litecoin transasction")
		total_account_value = auth.get_total_account_value()



		# primary_account = auth.get_primary_account()
		# primary_transactions = get_primary_transactions()
		# print(all_transactions, 'ALL TRANSACTIONS')
		# print(primary_transactions, 'ALL PRIMARY')
		# primary_account.refresh()


		# balance = primary_account.balance
		# context = {'primary_account':primary_account, 'all_transactions':all_transactions, 'primary_transactions':primary_transactions}
		context = {'past_buysell_transactions':newlist, 'account_value':total_account_value}
		return render(request, 'cryptoclient/profile.html', context)

class WalletSendMoneyView(View):
	pass
	# primary_account.send_money(to=address.address, amount='0.01', currency='BTC', description='For being awesome!')
	

class SwapCryptoWalletView(View):
	
	def get(self, request):
		coinigy = CoinigyAPI()
		binance2 = Binance2Auth()
		gdax = GDAXApi()

		tickers = binance2.get_all_tickers()
		for item in tickers:
			# print(item)
			symbol = item['symbol']
			# print(symbol)
			

		balances = coinigy.list_balances()

		

		# print(balances)

		crypto_list = binance2.every_crypto_binance()

		# for item in crypto_list:
		# 	address = binance2.get_deposit_address(item)
		# 	print(item, type(address), address)
		# 	user_address = UserAddresses()
		# 	if address['success'] == False:
		# 		continue

		# 	else:
				
		# 		print(address)
			

		# 		print(item, address['address'], len(address['address']))
		# 		user_address.crypto = item
		# 		user_address.address = address['address']
		# 		user_address.save()



		# 	time.sleep(3)

		user_addresses = UserAddresses.objects.all()
		print(user_addresses)
		# for item in user_addresses:
		# 	print(item.address, item.crypto)


		print(balances,"right here")

		context = {
			'balances': balances,
			'user_addresses': user_addresses
		}

		return render(request, 'cryptoclient/swap-crypto-wallet.html', context)



class SwapCryptoView(View):

	form_class = CryptoToCryptoForm
	form_class2 = ChartForm

	def get(self, request):

		cryptotocryptoform = self.form_class()
		chart_form = self.form_class2()





		# coinigy = CoinigyAPI()

		# history = coinigy.list_history_data()
		# print(history)

		# orders = coinigy.list_orders()
		# print(orders)

		# auth = coinigy.list_accounts()
		# # print(auth['data'][0])
		# auth_id, exch_id, = coinigy.get_auth_and_exch_id()
		# # print(auth_id,exch_id)

		# balances = coinigy.list_balances()
		# exchanges = coinigy.list_exchanges()
		# markets = coinigy.list_markets()
		# order_type, price_type = coinigy.get_ordertype_pricetype_id()

		order_types = {'1':'Buy', '2':'Sell'}
		price_types = {'3':'Limit', '6':'Stop Limit'}
		# print(order_type, price_type)
		# exchanges = exchanges['data']
		# print(exchanges, 'exchange')
		# print(markets, 'market')
		

		# exch_code = ''
		# for exchange in exchanges:
		# 	if exchange['exch_name'] == 'Binance':
		# 		exch_code = exchange['exch_code']







		# coins = shapeshift.get_coins()
		
		# rate = shapeshift.get_rate('btc_ltc')

		# create_order = coinigy.create_order(auth_id, exch_id, )
		# create_order(self, auth_id, exch_id, mkt_id, order_type_id,price_type_id,limit_price, order_quantity):
		
		context = {
			# 'auth':auth['data'][0],
			# 'balances':balances['data'],
			'form':cryptotocryptoform,
			'chart_form': chart_form,
			# 'orders':orders['data']
		}

		return render(request, 'cryptoclient/swap-crypto.html', context)

	def post(self, request):

		print(request.body, "here")
		parsed_body = request.body.decode('ascii')
		print(parsed_body)
		split_body = parsed_body.split("&")
		print(split_body)
		requested_pair_data = split_body[1]
		requested_pair = requested_pair_data.split("=")
		just_requested_pair = requested_pair[1]
		print(just_requested_pair)


		coinigy = CoinigyAPI()
		binance = Binance2Auth()

		# auth_id, exch_id, = coinigy.get_auth_and_exch_id()
		order_types = coinigy.get_ordertype_pricetype_id()
		order_type_id = order_types['data']['order_types']
		# price_type_id = order_types['data']['price_types']
		# not going to allow limit trading.
		price_type_id = '3'

		# print('XOXOXOXOXOXOXO')
		# print(order_types['data'], 'order_type')
		# exchanges = coinigy.list_exchanges()
		
		# print(exchanges, 'exchange')
		# print(markets, 'market')
		# exchange = exchanges['data']

		# exch_code = ''
		# for item in exchange:
		# 	if item['exch_name'] == 'Binance':
		# 		exch_code = item['exch_code']



		# pairs = coinigy.list_markets(exch_code)
		# print(pairs)

		cryptotocryptoform = self.form_class(request.POST)
		# print(request.POST, 'post req')


		if cryptotocryptoform.is_valid():

			# order = coinigy.create_order(auth_id, exch_id, mkt_id, order_type_id, price_type_id, limit_price, order_quantity)
			user_pair_data = str(request.POST['pair'])
			limit_price = request.POST['price']
			price_type_id = request.POST['price_type']
			order_quantity = request.POST['order_quantity']
			order_type_id = request.POST['order_type']

			print(order_type_id, type(order_type_id))

			order_type_id1 = ''
			
			if order_type_id == '1':
				order_type_id1 = 'Buy'

			if order_type_id == '2':
				order_type_id1 = 'Sell'

			print(order_type_id1, type(order_type_id1))
			
			

		
			# mkt_id = ''
			# # print(pairs['data'], 'print')
			# print(pairs)
			
			# for item in pairs['data']:
			# 	# print(item)

			# 	if user_pair_data == str(item['mkt_name']):
			# 		mkt_id = item['mkt_id']
			# 		# print(mkt_id,'mkt_id')

			print(order_type_id1, price_type_id, type(order_type_id1), type(price_type_id),"______________________")


			if order_type_id1 == 'Buy' and price_type_id == 'Limit':

				binance.create_buylimit_order(user_pair_data, order_quantity, limit_price)
				print('executed')
			elif order_type_id1 == 'Sell' and price_type_id == 'Limit':
				binance.create_selllimit_order(user_pair_data, order_quantity, limit_price)
				print('executed')
			elif order_type_id1 == 'Buy' and price_type_id == 'Market':
				binance.create_buymarket_order(user_pair_data, order_quantity, limit_price)
				print('executed')
			elif order_type_id1 == 'Sell' and price_type_id == 'Market':
				binance.create_sellmarket_order(user_pair_data, order_quantity, limit_price)
				print('executed')
			# print(auth_id, exch_id, mkt_id, order_type_id, price_type_id, limit_price, order_quantity, "right before order creation")
			# order = coinigy.create_order(int(auth_id), int(exch_id), int(mkt_id), int(order_type_id), price_type_id, float(limit_price), float(order_quantity))
			# print(order)
			# order = binance.create_limit_order(user_pair_data, order_quantity, limit_price)
			
			# print(order)
			return redirect('cryptoclient:swap-crypto')
		# elif ChartForm.is_valid():


		else:
			return HttpResponse('Didnt Work')

class SwapCryptoSendMoneyView(View):
	
	form_class = SwapCryptoSendMoneyForm

	def get(self, request):

		send_form = self.form_class()

		context = {
			"form":send_form
		}

		return render(request, 'cryptoclient/swap-crypto-send-money.html', context)

	def post(self,request):

		swapcryptoform = self.form_class(request.POST)

		if swapcryptoform.is_valid():


			address = request.POST['to_address']
			amount = request.POST['amount']
			currency = request.POST['currency']
			print(address, amount, currency)
			binance = Binance2Auth()

			send_form = binance.withdraw_binance(currency, address, amount)
			return redirect('cryptoclient:swap-crypto')

		else:

			return HttpResponse('Didnt Work')


class SwapCryptoOrderView(View):

	form_class = DeleteOrderForm

	def get(self, request):

		binance = BinanceAPI()
		binance2 = Binance2Auth()

		form = self.form_class()
		

		
		orders2 = binance2.get_open_orders()
		print(orders2)
		

		# orders = binance.get_current_open_orders()

		# print(orders)

		context = {
			'orders':orders2,
			'form':form
		}

		return render(request, 'cryptoclient/swap-crypto-orders.html', context)

	def post(self, request):

		deleteform = self.form_class(request.POST)
		print(request.POST)

		binance = BinanceAPI()
		binance2 = Binance2Auth()



		# orders = binance.get_current_open_orders()

		# print(orders)
		# return HttpResponse("YES")

		if deleteform.is_valid():
			order_id = request.POST['orderId']
			symbol = request.POST['symbol']


			# binance.delete_order(order_id)
			binance2.cancel_order(order_id, symbol)

			return redirect('cryptoclient:swap-crypto-order')

		else:
			return HttpResponse('Didnt Work')










