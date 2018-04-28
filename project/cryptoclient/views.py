from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from cryptoclient.wrapper_coinbase import Wallet
from cryptoclient.wrapper_gdax import GDAXApi
from cryptoclient.wrapper_shapeshift import CoinigyAPI

from cryptoclient.form import WalletCreationForm, LimitOrderForm, CryptoToCryptoForm, WalletSendMoneyForm, BetweenGDAXAndCBForm

# Create your views here.

class OptionListView(View):
	
	def get(self, request):
		GDAX = GDAXApi()
		bitcoin_data, ethereum_data = GDAX.market_data()
		# print(bitcoin_data, "1")
		# print(ethereum_data, "2")
		context = {
			'bitcoin_data':bitcoin_data,
			'ethereum_data':ethereum_data
		}
		return render(request, 'cryptoclient/option.html', context)

class WalletListView(View):

	def get(self, request):

		auth = Wallet()

		
		list_wallets = auth.list_wallets()
		# list_wallets = list_wallets['data']
		
		

		# list_wallets = auth.get_addresses()
		# print(auth.get_addresses(), "walletlistview")
		print(list_wallets, "list_wallets")

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
			# print(name)
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
		print(list_wallets)
		
		

		list_address = auth.get_addresses()
		# print(list_address)
		# print(auth.get_addresses(), "walletlistview")

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


			send_money = auth.send_money(account_id, address, amount, crypto)
			print(send_money)

			return redirect('cryptoclient:wallet-list')

		else:
			return render(request, self.template_name, {'form': wallettransactionform})

class WalletCoinbaseGDAXTransferView(View):

	template_name = 'cryptoclient/wallet-transaction-gdax.html'
	form_class = BetweenGDAXAndCBForm

	def get(self, request):

		transfer_form = self.form_class()
		
		context = {
			'form':transfer_form
		}

		return render(request, self.template_name, context)

	def post(self, request):
		GDAX = GDAXApi()
		data = request.POST
		transfer_form = self.form_class(request.POST)

		# get coinbase accounts
		# match the accounts with the currency they chose


		if transfer_form.is_valid():
			amount = request.POST['amount']
			currency = request.POST['currency']
			transaction_type = request.POST['transaction']

			if transaction_type == "1":
				GDAX.withdraw_to_coinbase(amount, currency, coinbase_account_id)
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
		print("XOXOXOXOXOXOXOOXOXOXOXOXO")

		all_open_orders = GDAX.get_all_open_orders()


		# if price > crypto_price['price']:
		# 	stop = 'loss'

		# elif price < crypto_price['price']:
		# 	stop = 'entry'
		# order = GDAX.create_order()

		context = {
			'accounts':accounts,
			'form':purchaseorderform,
			'crypto_pairs':crypto_pairs,
			'open_orders':all_open_orders
		}

		return render(request, 'cryptoclient/buy-sell.html', context)

	# ORDER_CHOICES = (
 #    (1, ("Market Order")),
 #    (2, ("Limit Order"))
    
	# )
	# SIDE_CHOICES = (
	#     (1, ("Buy")),
	#     (2, ("Sell"))
	# )

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

class BuySellOrderView(View):

	def get(self,request):
		GDAX = GDAXApi()

		all_open_orders = GDAX.get_all_open_orders()


		# if price > crypto_price['price']:
		# 	stop = 'loss'

		# elif price < crypto_price['price']:
		# 	stop = 'entry'
		# order = GDAX.create_order()

		context = {
			
			'open_orders':all_open_orders
		}

		return render(request, 'cryptoclient/buy-sell-order.html', context)

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
		auth = Wallet()

		# all_transactions = auth.get_all_transactions()

		all_accounts = auth.get_accounts()
		# print(all_accounts, "all accounts")
		litecoin_id = all_accounts['data'][2]['id']
		bitcoin_id = all_accounts['data'][4]['id']
		bitcoin_cash_id = all_accounts['data'][0]['id']
		ethereum_id = all_accounts['data'][3]['id']
		usd_id = all_accounts['data'][1]['id']

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
		context = {'litecoin_transactions':litecoin_transactions['data'], 'account_value':total_account_value}
		return render(request, 'cryptoclient/profile.html', context)

class WalletSendMoneyView(View):
	pass
	# primary_account.send_money(to=address.address, amount='0.01', currency='BTC', description='For being awesome!')
		
class SwapCryptoView(View):

	form_class = CryptoToCryptoForm

	def get(self, request):

		cryptotocryptoform = self.form_class()





		coinigy = CoinigyAPI()

		orders = coinigy.list_orders()
		print(orders)

		auth = coinigy.list_accounts()
		# print(auth['data'][0])
		auth_id, exch_id, = coinigy.get_auth_and_exch_id()
		# print(auth_id,exch_id)

		balances = coinigy.list_balances()
		exchanges = coinigy.list_exchanges()
		# markets = coinigy.list_markets()
		order_type, price_type = coinigy.get_ordertype_pricetype_id()

		order_types = {'1':'Buy', '2':'Sell'}
		price_types = {'3':'Limit', '6':'Stop Limit'}
		print(order_type, price_type)
		exchanges = exchanges['data']
		# print(exchanges, 'exchange')
		# print(markets, 'market')
		

		exch_code = ''
		for exchange in exchanges:
			if exchange['exch_name'] == 'Binance':
				exch_code = exchange['exch_code']







		# coins = shapeshift.get_coins()
		
		# rate = shapeshift.get_rate('btc_ltc')

		# create_order = coinigy.create_order(auth_id, exch_id, )
		# create_order(self, auth_id, exch_id, mkt_id, order_type_id,price_type_id,limit_price, order_quantity):
		
		context = {
			'auth':auth['data'][0],
			'balances':balances['data'],
			'form':cryptotocryptoform,
			'orders':orders['data']
		}

		return render(request, 'cryptoclient/swap-crypto.html', context)

	def post(self, request):

		coinigy = CoinigyAPI()
		auth_id, exch_id, = coinigy.get_auth_and_exch_id()
		order_types = coinigy.get_ordertype_pricetype_id()
		order_type_id = order_types['data']['order_types']
		# price_type_id = order_types['data']['price_types']
		# not going to allow limit trading.
		price_type_id = '3'

		print('XOXOXOXOXOXOXO')
		print(order_types['data'], 'order_type')
		exchanges = coinigy.list_exchanges()
		
		# print(exchanges, 'exchange')
		# print(markets, 'market')
		exchange = exchanges['data']

		exch_code = ''
		for item in exchange:
			if item['exch_name'] == 'Binance':
				exch_code = item['exch_code']



		pairs = coinigy.list_markets(exch_code)

		cryptotocryptoform = self.form_class(request.POST)
		# print(request.POST, 'post req')


		if cryptotocryptoform.is_valid():

			# order = coinigy.create_order(auth_id, exch_id, mkt_id, order_type_id, price_type_id, limit_price, order_quantity)
			user_pair_data = str(request.POST['pair'])
			limit_price = request.POST['price']
			price_type_id = request.POST['price_type']
			order_quantity = request.POST['order_quantity']
			order_type_id = request.POST['order_type']

			if order_type_id == 1:
				order_type_id == 'Buy'

			if order_type_id == 2:
				order_type_id == 'Sell'

		
			mkt_id = ''
			# print(pairs['data'], 'print')
			
			for item in pairs['data']:
				# print(item)

				if user_pair_data == str(item['mkt_name']):
					mkt_id = item['mkt_id']
					# print(mkt_id,'mkt_id')

			print(auth_id, exch_id, mkt_id, order_type_id, price_type_id, limit_price, order_quantity, "right before order creation")
			order = coinigy.create_order(auth_id, exch_id, mkt_id, order_type_id, price_type_id, limit_price, order_quantity)
			print(order)
			print('executed')
			return redirect('cryptoclient:swap-crypto')
		else:
			return HttpResponse('Didnt Work')



