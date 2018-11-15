from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.views.generic import View
from datetime import date, datetime
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
from cryptoclient.models import UserAddresses, UserCredentials, UserBinanceOrders, UserGdaxOrders
from cryptoclient.credentials import get_current_user
# from cryptoclient.tasks import save_address

from cryptoclient.form import WalletCreationForm, LimitOrderForm, CryptoToCryptoForm, WalletSendMoneyForm, BetweenGDAXAndCBForm, ChartForm, SwapCryptoSendMoneyForm, DeleteOrderForm, SubmitKeysForm, MarketOrderForm

# Create your views here.

class OptionListView(View):
	
	def get(self, request):
		get_current_user(request.user.id)
		print('line33')

		GDAX = GDAXApi()
		bitcoin_data, ethereum_data = GDAX.market_data()
		
		print('over here')
		BTC_data = GDAX.get_24_hour_data('BTC-USD')
		ETH_data = GDAX.get_24_hour_data('ETH-USD')
		print('line 39')

		print(BTC_data)

		context = {
			'bitcoin_data':bitcoin_data,
			'ethereum_data':ethereum_data,
			'BTC_daily':BTC_data,
			'ETH_daily':ETH_data
		}
		return render(request, 'cryptoclient/option.html', context)

class SubmitKeyView(View):

	form_class = SubmitKeysForm

	def get(self, request):
		print(request.user, type(request.user))
		get_current_user(request.user.id)
		form = self.form_class()


		print(request.user.id, "user_id")

		context = {
			'form':form
		}

		return render(request, 'cryptoclient/submit-keys.html', context)

	def post(self, request):
		# now = datetime.datetime.now()
		# now_plus_2_years = now + datetime.timedelta(weeks = 100)

		# new_years_2019 = datetime.datetime(2019, 1, 1)
		get_current_user(request.user.id)
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
		

		print('right before form')
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
			# save_address(request.user.id)

			return redirect('cryptoclient:submit-key')
		
		else:
			
			context = {
				'form':form1
			}

			return render(request, 'cryptoclient/submit-keys.html', context)




class WalletListView(View):

	def get(self, request):
		get_current_user(request.user.id)
		# save_address(request.user.id)

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
		get_current_user(request.user.id)
		walletcreationform = self.form_class()
		context = {
			"form": walletcreationform
		} 
		
		return render(request, self.template_name, context)

	def post(self, request):
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
		transaction_form = self.form_class()

		
		context = {
			'form':transaction_form
		}

		return render(request, self.template_name, context)

	def post(self, request):
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
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

		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
		purchaseorderform = self.form_class(request.POST)

		GDAX = GDAXApi()
		test = type(request.POST['order_type'])
		# print(test)
		another_str = int(request.POST['order_type'])
		# print(another_str)
		# print(request.POST)

		obj = User.objects.get(pk=request.user.id)

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
		# print(order_type, order_side, crypto_pair, price, amount, "POST")

		# print(order_type,"type", order_side,"buyorsell")
		gdax_orders = UserBinanceOrders()


		if purchaseorderform.is_valid():
			
			if order_type == "limit":
				order = GDAX.create_limit_order(order_side, price, crypto_pair, amount, order_type)
				
				gdax_orders.crypto_pair = crypto_pair
				gdax_orders.order_type = order_type
				gdax_orders.buy_or_sell = order_side
				gdax_orders.price = float(order)
				gdax_orders.amount = float(amount)
				gdax_orders.exchange = "GDAX"
				gdax_orders.user = obj
				gdax_orders.save()
				print(order, "limit")

			elif order_type == "market":
		
				# print(order_side, order_type, crypto_pair, amount, order1, price)
				# print(type(order_side), type(order_type), type(crypto_pair), type(amount), type(order1), type(price))

				order1 = GDAX.create_market_order(order_side, order_type, crypto_pair, amount)

				# print(order_side, order_type, crypto_pair, amount, order1, price)
				# print(type(order_side), type(order_type), type(crypto_pair), type(amount), type(order1), type(price))
				

				gdax_orders.crypto_pair = crypto_pair
				gdax_orders.order_type = order_type
				gdax_orders.buy_or_sell = order_side
				gdax_orders.price = float(order1)
				gdax_orders.amount = float(amount)
				gdax_orders.exchange = "GDAX"
				gdax_orders.user = obj
				gdax_orders.save()
				# print(order, "market")

			return redirect('cryptoclient:buy-sell')

		else:
			print('form is broken')
			return redirect('cryptoclient:buy-sell')

class BuySellDataView(View):

	def get(self, request):
		print("just got into the data")
		get_current_user(request.user.id)
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

class BuySellLTCDataView(View):

	def get(self, request):
		print("just got into the data")
		get_current_user(request.user.id)
		GDAX = GDAXApi()


		start = date(2017, 12, 4).isoformat()
		end = date(2018, 7, 3).isoformat()
		# print(start, end)
		# style.use('ggplot')
		granularity = '86400'
		LTC_candle_data = GDAX.get_candle_data(start, end, granularity, 'LTC-USD')
		# ETH_candle_data = GDAX.get_candle_data(start, end, granularity, 'ETH-USD')
		# LTC_candle_data = GDAX.get_candle_data(start, end, granularity, 'LTC-USD')
		# print(ETH_candle_data)
		# print(BTC_candle_data)
		LTC_close_data = GDAX.get_close_data(LTC_candle_data)
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
		LTC_close_data.insert(0, 'LTC')
		# ETH_close_data.insert(0, 'ETH')
		# LTC_close_data.insert(0, 'LTC')
		# print(LTC_close_data)
		# crypto_json['LTC'] = LTC_close_data
		crypto_json['LTC'] = LTC_close_data
		# crypto_json['ETH'] = ETH_close_data

		
		# print(ltc_json)
		print(crypto_json, "wow")
		return JsonResponse(crypto_json)

class BuySellOrderView(View):

	form_class = DeleteOrderForm

	def get(self,request):
		get_current_user(request.user.id)
		GDAX = GDAXApi()

		form = self.form_class()

		all_open_orders = GDAX.get_all_open_orders()


		# if price > crypto_price['price']:
		# 	stop = 'loss'

		# elif price < crypto_price['price']:
		# 	stop = 'entry'
		# order = GDAX.create_order()

		print(all_open_orders)

		context = {
			'form':form,
			'open_orders':all_open_orders
		}

		return render(request, 'cryptoclient/buy-sell-order.html', context)

	def post(self, request):
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)

		obj = User.objects.get(pk=request.user.id)

		# all_gdax_orders = UserGdaxOrders.objects.all()
		all_binance_orders = UserBinanceOrders.objects.all()
		# print(all_binance_orders)

		# current_user_gdax_orders = all_gdax_orders.filter(user=obj)
		current_user_binance_orders = all_binance_orders.filter(user=obj)

		print(current_user_binance_orders)

		











		# list_of_all_pastbuysell_transactions = []
		# auth = Wallet()
		# gdax = GDAXApi()
		# list_of_all_GDAX_pairs = ["BTC-USD", "ETH-USD", "LTC-USD"]
		
		# for item in list_of_all_GDAX_pairs:

		# 	fills = gdax.list_fills(item)
		# 	print(fills)

		# binance = BinanceAPI()
		# coinigy = CoinigyAPI()
		# balances = coinigy.list_balances()
		# balances = balances['data']

		# # binance_data = binance.get_past_trades()
		# # print(binance_data)
		# ticker_data = binance.ticker()
		# # print(ticker_data, "thisthisthisthis")
		# ticker_list = []

		# for ticker in ticker_data:
		# 	ticker_list.append(ticker['symbol'])
		# print(ticker_list)

		# for ticker in ticker_list:
		# 	trades = binance.old_trades(ticker)
			# print(trades)



		# these are just the pastbuysell

		# all_transactions = auth.get_all_transactions()

		

		# all_accounts = auth.get_accounts()
		# # print(all_accounts, "all accounts")
		# litecoin_id = all_accounts['data'][2]['id']
		# bitcoin_id = all_accounts['data'][4]['id']
		# bitcoin_cash_id = all_accounts['data'][0]['id']
		# ethereum_id = all_accounts['data'][3]['id']
		# usd_id = all_accounts['data'][1]['id']

		# list_of_all_ids = [litecoin_id, bitcoin_id, bitcoin_cash_id, ethereum_id]

		# for crypto_id in list_of_all_ids:
		# 	transactions = auth.get_all_transactions(crypto_id)

		# 	number_of_transaction = len(transactions['data'])

		# 	for transaction in range(0, number_of_transaction-1):
		# 		# print(transactions['data'], "RIGHT HERE")
		# 		list_of_all_pastbuysell_transactions.append(transactions['data'][transaction])



		# print(list_of_all_pastbuysell_transactions, "alltransaction")

		# newlist = sorted(list_of_all_pastbuysell_transactions, key=lambda k: k['created_at'], reverse=True) 

		# # print(newlist, "right here")


		# litecoin_transactions = auth.get_all_transactions(litecoin_id)
		# bitcoin_transactions = auth.get_all_transactions(bitcoin_id)
		# bitcoin_cash_transactions = auth.get_all_transactions(bitcoin_cash_id)
		# ethereum_transactions = auth.get_all_transactions(ethereum_id)
		# usd_transactions = auth.get_all_transactions(usd_id)
		# # print(litecoin_transactions['data'], "litecoin transasction")
		# total_account_value = auth.get_total_account_value()



		# primary_account = auth.get_primary_account()
		# primary_transactions = get_primary_transactions()
		# print(all_transactions, 'ALL TRANSACTIONS')
		# print(primary_transactions, 'ALL PRIMARY')
		# primary_account.refresh()


		# balance = primary_account.balance
		# context = {'primary_account':primary_account, 'all_transactions':all_transactions, 'primary_transactions':primary_transactions}

		print(current_user_binance_orders)
		# current_user_binance_orders = current_user_binance_orders.reverse()
		# final_list = []

		# for item in current_user_binance_orders:
		# 	final_list.append(item)

		# print(final_list)

		# final_list = final_list.reverse()

		# print(final_list)

		current_user_binance_orders = current_user_binance_orders.reverse()[:5]


		context = {
			'past_orders':current_user_binance_orders
		}
		return render(request, 'cryptoclient/profile.html', context)

class WalletSendMoneyView(View):
	pass
	# primary_account.send_money(to=address.address, amount='0.01', currency='BTC', description='For being awesome!')
	

class SwapCryptoWalletView(View):
	
	def get(self, request):
		get_current_user(request.user.id)
		coinigy = CoinigyAPI()
		binance2 = Binance2Auth()
		gdax = GDAXApi()

		# tickers = binance2.get_all_tickers()
		list_of_main_cryptos = ['BTC', 'ETH', 'LTC', 'ETC']
		# for item in tickers:
		# 	# print(item)
		# 	symbol = item['symbol']
		# 	# print(symbol)
			

		balances = coinigy.list_balances()

		

		# print(balances)

		crypto_list = binance2.every_crypto_binance()
		list_of_final_balances = []

		for item in list_of_main_cryptos:
			address = binance2.get_deposit_address(item)
			cryptoaddress = {
				'crypto':item,
				'address':address
			}
			list_of_final_balances.append(cryptoaddress)

			time.sleep(1)
		# 	address = binance2.get_deposit_address(item)
		# 	print(item, type(address), address, "hererereerer")
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
		# print(balances,"right here")
		# list_of_balances = balances['data']
		# print(list_of_balances, 'list_of_balances')
		# list_of_crypto_balance_symbol = []

		# for balance in list_of_balances:
		# 	list_of_crypto_balance_symbol.append(balance['balance_curr_code'])

		# # print(list_of_balances)
		# user_addresses = UserAddresses.objects.filter(address__lte=20)
		

		# list_of_crypto_addresses = []
		# list_of_no_addresses = []
		# # print(list_of_crypto_balances)
		# for item in list_of_crypto_balance_symbol:
			
			
		# 	cryptoaddress = user_addresses.filter(crypto=item)
		# 	print(cryptoaddress)
		# 	# print(cryptoaddress)
		# 	if cryptoaddress.exists():
		# 		cryptoaddress = cryptoaddress[0]
		# 		list_of_crypto_addresses.append(cryptoaddress)

		# 	else:
		# 		list_of_no_addresses.append(item)
				

			
				
		# print(list_of_no_addresses)
		# list_of_final = []

		# for item in list_of_balances:
		# 	if item in list_of_no_addresses:
		# 		returnvalue = list_of_balances.pop()

		# # print(list_of_balances)
		# print(list_of_crypto_addresses, 'crypto_addresses')

		# for item in range(0, len(list_of_balances)-1):
			
		# 	current_crypto = list_of_balances[item]
		# 	print(current_crypto, "sdssds")
		# 	print(list_of_balances[item]['balance_amount_avail'])
		# 	available = list_of_balances[item]['balance_amount_avail']
		# 	total = list_of_balances[item]['balance_amount_total']



		# 	final_list = {

		# 		'crypto': list_of_crypto_balances[item],
		# 		'address': list_of_crypto_addresses[item].address,
		# 		'current_holding': available,
		# 		'total_holding': total
		# 	}

		# 	list_of_final.append(final_list)

		# # list_of_excluded = UserAddresses.
		# final_list_excluded = ""

		# # for item in list_of_final:
		# # 	addresses = UserAddresses.objects.exclude(crypto=item)
		# # 	final_list_excluded = ad

		# for item in range(0,len(list_of_final)-1):
		# 	if len(final_list_excluded) == 0:
		# 		addresses = UserAddresses.objects.exclude(crypto=list_of_final[item])
		# 		final_list_excluded = addresses

		# 	final_list_excluded = final_list_excluded.exclude(crypto=list_of_final[item])

		
		# print(final_list_excluded) 
		# list_of_excluded = []


		# for item in range(0, len(final_list_excluded)-1):
			
		# 	user_address = final_list_excluded[item]
			

		# 	list_of_excluded.append(user_address)


		

		# zero = '0.0000'
		

		context = {
			'balances': balances,
			'user_addresses': list_of_final_balances,
			# 'list_of_excluded': list_of_excluded,
			# 'zero': zero
		}

		return render(request, 'cryptoclient/swap-crypto-wallet.html', context)

class SwapCryptoAddressView(View):

	# Need to get all the tickers for 

	def get(self, request):
		get_current_user(request.user.id)
		coinigy = CoinigyAPI()
		binance2 = Binance2Auth()

		crypto_list = binance2.every_crypto_binance()

		balances = coinigy.list_balances()
		# print(balances)
		balances = balances['data']
		print(balances)
		list_of_only_holding_symbol = []
		for item in balances:
			list_of_only_holding_symbol.append(item['balance_curr_code'])

		final_list = []

		for crypto in crypto_list:
			if crypto in list_of_only_holding_symbol:
				for item in balances:
					if item['balance_curr_code'] == crypto:
						balance_current = item['balance_amount_avail']
						balance_total = item['balance_amount_total']

						temporary_dict = {
							'crypto':crypto,
							'balance_current':balance_current,
							'balance_total' : balance_total
						}
						final_list.append(temporary_dict)

			else:

				temporary_dict = {
							'crypto':crypto,
							'balance_current':"0.00000",
							'balance_total': "0.00000"
						}

				final_list.append(temporary_dict)

		context = {
			'final_list':balances
		}

			
		return render(request, 'cryptoclient/swap-crypto-address.html', context)





class SwapCryptoView(View):

	form_class = CryptoToCryptoForm
	form_class2 = MarketOrderForm

	def get(self, request):
		get_current_user(request.user.id)
		cryptotocryptoform = self.form_class()
		market_order_form = self.form_class2()
		binance = Binance2Auth()
		tickers = binance.get_all_tickers()
		print(tickers)





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
			'market_form': market_order_form,
			# 'orders':orders['data']
		}

		return render(request, 'cryptoclient/swap-crypto.html', context)

	def post(self, request):
		get_current_user(request.user.id)
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

		binance_orders = UserBinanceOrders()

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

		obj = User.objects.get(pk=request.user.id)
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
				binance_orders.crypto_pair = user_pair_data
				binance_orders.order_type = price_type_id
				binance_orders.buyorsell = order_type_id1
				binance_orders.price = limit_price
				binance_orders.amount = order_quantity
				binance_orders.user = obj
				binance_orders.exchange = "Binance"
				binance_orders.save()
				
				print('executed')



			elif order_type_id1 == 'Sell' and price_type_id == 'Limit':
				binance.create_selllimit_order(user_pair_data, order_quantity, limit_price)
				binance_orders.crypto_pair = user_pair_data
				binance_orders.order_type = price_type_id
				binance_orders.buyorsell = order_type_id1
				binance_orders.price = limit_price
				binance_orders.amount = order_quantity
				binance_orders.exchange = "Binance"
				binance_orders.user = obj
				binance_orders.save()

				print('executed')



			elif order_type_id1 == 'Buy' and price_type_id == 'Market':
				price = binance.create_buymarket_order(user_pair_data, order_quantity)
				binance_orders.crypto_pair = user_pair_data
				binance_orders.order_type = price_type_id
				binance_orders.buyorsell = order_type_id1
				binance_orders.price = price
				binance_orders.amount = order_quantity
				binance_orders.exchange = "Binance"
				binance_orders.user = obj
				binance_orders.save()

				print('executed')



			elif order_type_id1 == 'Sell' and price_type_id == 'Market':
				price = binance.create_sellmarket_order(user_pair_data, order_quantity)
				binance_orders.crypto_pair = user_pair_data
				binance_orders.order_type = price_type_id
				binance_orders.buyorsell = order_type_id1
				binance_orders.exchange = "Binance"
				binance_orders.price = price
				binance_orders.amount = order_quantity
				binance_orders.user = obj
				binance_orders.save()

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
		get_current_user(request.user.id)
		send_form = self.form_class()

		context = {
			"form":send_form
		}

		return render(request, 'cryptoclient/swap-crypto-send-money.html', context)

	def post(self,request):
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
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
		get_current_user(request.user.id)
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

class SwapCryptoPricesView(View):

	def get(self, request):

		binance = Binance2Auth()
		tickers = binance.get_all_tickers()
		print(tickers)

		context = {
			'tickers':tickers
		}

		return render(request, 'cryptoclient/swap-crypto-prices.html', context)










