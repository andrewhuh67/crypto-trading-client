from django import forms

class WalletCreationForm(forms.Form):
	name = forms.CharField(max_length=20)

class MoneyTransfer(forms.Form):
	# find the max length of the address
	address = forms.CharField(max_length=40)
	# possibly a float field
	amount = forms.CharField(max_length=20)
	currency = forms.CharField(max_length=40)
	description = forms.CharField(max_length=30)
