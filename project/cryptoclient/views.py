from django.shortcuts import render
from django.views.generic import View
from cryptoclient.wrapper_coinbase import Wallet
from cryptoclient.wrapper_gdax import GDAXApi

from cryptoclient.form import WalletCreationForm, PurchaseOrderForm

# Create your views here.

class OptionListView(View):
	
	def get(self, request):
		return render(request, 'cryptoclient/option.html')

class WalletListView(View):

	def get(self, request):

		auth = Wallet()

		# auth = CoinbaseWalletAuth(API_KEY, API_SECRET)
		# authorized_req = auth(request)
		list_wallets = auth.list_wallets()
		list_wallets = list_wallets['data']
		# print(list_wallets, "WALLETLISTVIEW")

		context = {
			"wallets": list_wallets
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

class BuySellView(View):

	form_class = PurchaseOrderForm

	def get(self,request):
		purchaseorderform = self.form_class()
		GDAX = GDAXApi()

		accounts = GDAX.get_accounts()
		crypto_pairs = GDAX.get_crypto_pairs()
		# order = GDAX.create_order()
		print(accounts, crypto_pairs)

		context = {
			'accounts':accounts,
			'form':purchaseorderform,
			'crypto_pairs':crypto_pairs
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

		print(purchaseorderform)
		print(request.POST, 'request.POST')
		if request.POST['order_type'] == 1:
			request.POST['order_type'] = 'market'
		elif request.POST['order_type'] == 2:
			request.POST['order_type'] = 'limit'

		if request.POST['order_side'] == 1:
			request.POST['order_side'] = 'buy'
		elif request.POST['order_side'] == 2:
			request.POST['order_side'] = 'sell'


		order_type = request.POST['order_type']
		order_side = request.POST['order_side']
		crypto_pair = request.POST['crypto_pair']
		price = request.POST['price']
		amount = request.POST['amount']

		if purchaseorderform.is_valid():
			
			order = GDAX.create_order(order_side, price, crypto_pair, amount)
			print(order)

			return HttpResponse()



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
		


