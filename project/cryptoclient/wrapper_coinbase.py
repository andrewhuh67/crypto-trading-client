from coinbase.wallet.client import Client
from cryptoclient.credentials import CredentialsCB

credentials = CredentialsCB()

API_KEY = credentials.api_key()
# both these need to be in a seperate file later. before you push to github.
API_SECRET = credentials.api_secret()



class Wallet():
	
	def authenticate(self):
		client = Client(
			API_KEY,
			API_SECRET)
		if client:
			print(client, "client wrapper")
			return client
		else:
			print("authentication failed")

	def list_wallets(self):
		auth = self.authenticate()

		accounts = auth.get_accounts()
		# print(accounts.data, "account data line 33")
		return accounts

	def create_wallet(self, name):
		auth = self.authenticate()

		account = auth.create_account(name=str(name))
		address = account.create_address()
		print(address, "address")
		print(dir(account), "dir")
		account.address = address
		balance = account.balance
		print("{}:{}{}--{}".format(account.name, balance.amount, balance.currency, account.address), "create_wallet")
		return account.address

	def get_primary_account(self):

		auth = self.authenticate()
		primary_account = auth.get_primary_account()
		print(primary_account)
		return primary_account

	def get_accounts(self):
		auth = self.authenticate()
		accounts = auth.get_accounts()
		
		return accounts

	def get_primary_transactions(self):
		auth = self.authenticate()
		primary_account = auth.get_primary_account()
		print(primary_account.get_transactions())
		transactions = primary_account.get_transactions()
		return transactions
	def get_all_transactions(self, account_id):
		auth = self.authenticate()
		
		print(auth.get_transactions(account_id))
		transactions = auth.get_transactions(account_id)
		return transactions

	def get_total_account_value(self):
		auth = self.authenticate()
		accounts = auth.get_accounts()['data']
		print(accounts)
		total_account_value = 0
		for account in accounts:
			total_account_value += float(account['native_balance']['amount'])
		return total_account_value

	def get_last_transaction(self):
		primary_account = self.get_primary_account()
		tranaction = primary_account.get_transactions()[-1]
		return transaction

	def send_money(self, address, amount, currency, description):
		primary_account = self.get_primary_account()
		primary_account.send_money(to=address.address, amount=amount, currency=currency, description=description)


	# def sell_coin(self, amount, currency):
	# 	pass

	# def buy_coin(self, amount, currency):
	# 	pass

	def get_orders(self):
		auth = self.authenticate()
		orders = auth.get_orders()
		return orders

	def get_addresses(self):
		auth = self.authenticate()
		accounts = auth.get_accounts()
		
		accounts = accounts['data']
		
		account_ids = {}
		for account in accounts:
			# print(account)
			acc = account['currency']
			# print(str(acc), "acc")

			account_ids[str(account['currency'])] = account['id']

		# print(account_ids, "account_ids")
		address_list = []
		for key in account_ids:
			print(key)
			if key == 'USD':
				continue
			# print(account_ids[key], "item")

			single_account_id = account_ids[key]
			address = auth.get_addresses(single_account_id)
			

			address = address['data'][0]
			# print(address, "address")
			address_list.append(address)
		print(address_list)
		return address_list

		# print(accounts['data'], "get_addresses")
		# accounts_data = accounts['data']
		# account_ids = []
		# account_currencies = []
		# for accounts in accounts_data:
		# 	# print(accounts['currency'])
		# 	account_currencies.append(accounts['currency'])
		# 	account_ids.append(accounts['id'])

		# accounts = zip(account_ids, account_currencies)

		# # print(accounts,'acc')

		# addresses = []
		# for key, value in accounts:
		# 	print(key, value)
		# 	address = auth.get_addresses(key)
		# 	# print(address,'addresssss')

		# 	empty_list = address['data']
		# 	# print(empty_list, "empty_list")
		# 	# print(empty_list, "eem")

		# 	if empty_list == [] and key != 'USD':
		# 		# print(address['data'], "data")
		# 		new_address = self.create_addresses(key)
		# 		empty_list.append(new_address)


		# 	print(address, "address")
		# 	addresses.append(address)
		# 	print(empty_list, "empty_list")

		# return addresses

	def create_addresses(self, account_id):
		auth = self.authenticate()
		address = auth.create_address(account_id)
		# print(address, "create-address")
		return address

	def delete_addresses(self,account_id):
		pass

	def send_money_coinbase_exchange(self, account_id, address, amount, currency):
		auth = self.authenticate()

		transaction = auth.send_money(account_id, address, amount, currency)

		return transaction





			


















