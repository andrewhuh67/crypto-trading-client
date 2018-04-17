from django import forms
from cryptoclient.choices import *

class WalletCreationForm(forms.Form):
	name = forms.CharField(max_length=20)


# maybe
class MoneyTransfer(forms.Form):
	# find the max length of the address
	address = forms.CharField(max_length=40)
	# possibly a float field
	amount = forms.CharField(max_length=20)
	currency = forms.CharField(max_length=40)
	description = forms.CharField(max_length=30)

class LimitOrderForm(forms.Form):
	
	

	order_type = forms.ChoiceField(choices=ORDER_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(),
                                required=True
                                )

	order_side = forms.ChoiceField(choices=SIDE_CHOICES, required=True)
	crypto_pair = forms.CharField(max_length=40)
	price = forms.FloatField()
	amount = forms.FloatField()
	
	

class MarketOrderForm(forms.Form):

	order_type = forms.ChoiceField(choices=ORDER_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(),
                                required=True
                                )
	order_side = forms.ChoiceField(choices=SIDE_CHOICES, required=True)
	crypto_pair = forms.CharField(max_length=40)
	
	amount = forms.FloatField()

class CryptoToCryptoForm(forms.Form):
	
	price = forms.CharField(max_length=30)
	order_type = forms.ChoiceField(choices=SIDE_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(),
                                required=True
                                )
	price_type = forms.CharField(max_length=30)
	order_quantity = forms.FloatField()
	pair = forms.CharField(max_length=30)
								




