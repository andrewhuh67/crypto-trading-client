from django.shortcuts import render
from django.views.generic import View
from cryptoclient.wrapper_coinbase import Wallet

from cryptoclient.form import WalletCreationForm

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
		print(list_wallets, "WALLETLISTVIEW")

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
			print(name)
			auth = Wallet()
			address = auth.create_wallet(name)
			return redirect(self.success_url)

		else:	
			return render(request, self.template_name, {'form': walletcreationform})

class BuySellView(View):

	def get(self,request):
		return render(request, 'cryptoclient/buy-sell.html')


class ProfileView(View):

	def get(self, request):
		auth = Wallet()

		# all_transactions = auth.get_all_transactions()

		all_accounts = auth.get_accounts()
		print(all_accounts, "all accounts")
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
		print(litecoin_transactions['data'], "litecoin transasction")
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
		


