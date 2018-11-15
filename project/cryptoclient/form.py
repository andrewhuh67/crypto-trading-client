from django import forms
from cryptoclient.choices import *
from django.core.validators import RegexValidator

my_validator = RegexValidator(r"[a-zA-Z]+$", "Your string should contain only letters in it.")

class WalletCreationForm(forms.Form):
	name = forms.CharField(max_length=20)


# maybe
class MoneyTransfer(forms.Form):
	# find the max length of the address
	address = forms.CharField(max_length=150)
	# possibly a float field
	amount = forms.CharField(max_length=20)
	currency = forms.CharField(max_length=40)
	description = forms.CharField(max_length=30)

class LimitOrderForm(forms.Form):
	
	

	order_type = forms.ChoiceField(choices=ORDER_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(
                                	attrs={'class':'form-control','cols': 10, 'rows': 20}),
                                required=True
                                )

	order_side = forms.ChoiceField(choices=SIDE_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(
                                	attrs={'class':'form-control'}),
                                required=True
                                )
	crypto_pair = forms.ChoiceField(choices=CRYPTO_FIAT_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(
                                	attrs={'class':'form-control',
                                	}),
                                required=True
                                )
	
	price = forms.CharField(max_length=30, widget=forms.NumberInput(
								attrs={'placeholder':'Leave Blank for Market',
								'class':'form-control'}), required=False)
	amount = forms.FloatField(widget=forms.NumberInput(
								attrs={'class':'form-control', 'placeholder':'Amount of Crypto'}))
	
	

class MarketOrderForm(forms.Form):

	order_type = forms.ChoiceField(choices=ORDER_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(
                                	attrs={'class':'order1'
                                		}),
                                required=True
                                )
	order_side = forms.ChoiceField(choices=SIDE_CHOICES, required=True)
	crypto_pair = forms.CharField(max_length=40)
	
	amount = forms.FloatField()

class CryptoToCryptoForm(forms.Form):
	
	price = forms.CharField(max_length=30, widget=forms.NumberInput(
								attrs={'placeholder':'Leave Blank for Market',
								'class':'form-control'}), required=False)
	order_type = forms.ChoiceField(choices=SIDE_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(
                                	attrs={'class':'form-control'}),
                                required=True
                                )
	price_type = forms.ChoiceField(choices=ORDER_CHOICES,
								label="",
                                initial='',
                                widget=forms.Select(
                                	attrs={'class':'form-control'}),
                                required=True
                                )
	order_quantity = forms.FloatField(widget=forms.NumberInput(
								attrs={'class':'form-control', 'placeholder':'Amount of Crypto'}))
	pair = forms.CharField(max_length=8, widget=forms.TextInput(
							attrs={'class':'form-control',
							'placeholder':'Ex. VETETH'}))

class WalletSendMoneyForm(forms.Form):

	to_address = forms.CharField(max_length=150, widget=forms.TextInput(
									attrs={'class':'form-control', 'placeholder':'Deposit Address'}))
	amount = forms.FloatField(widget=forms.NumberInput(attrs={
										'class':'form-control',
										'placeholder':'Amount in Crypto'
		}))
	currency = forms.ChoiceField(choices=CRYPTO_CHOICE,
								label="",
                                initial='',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True
                                )

class DeleteOrderForm(forms.Form):

	orderId = forms.CharField(max_length=50)
	symbol = forms.CharField(max_length=20)

class SwapCryptoSendMoneyForm(forms.Form):

	to_address = forms.CharField(max_length=150, widget=forms.TextInput(
									attrs={'class':'form-control', 'placeholder':'Deposit Address'}))
	amount = forms.FloatField(widget=forms.NumberInput(
								attrs={'class':'form-control', 'placeholder':'Amount of Crypto'}))
	currency = forms.CharField(max_length=15, widget=forms.TextInput(
								attrs={'class':'form-control', 'placeholder':'Ex. ETH'}))

class BetweenGDAXAndCBForm(forms.Form):

	amount = forms.FloatField(widget=forms.NumberInput(
							attrs={'class':'form-control',
							'placeholder':'Amount in Crypto'}))
	currency = forms.ChoiceField(choices=CRYPTO_CHOICE,
								label="",
                                initial='',
                                widget=forms.Select(attrs={'class':'form-control',
                                	}),
                                required=True
                                )

	transaction = forms.ChoiceField(choices=WITHDRAW_DEPOSIT,
								label="",
                                initial='',
                                widget=forms.Select(attrs={'class':'form-control'}),
                                required=True
                                )

class ChartForm(forms.Form):

	pair = forms.CharField(max_length=20)

class SubmitKeysForm(forms.Form):
	cb_api_key = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	cb_secret_key = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	gdax_api_key = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	gdax_secret_key = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	gdax_passphrase = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	coinigy_api_key = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	coinigy_api_secret = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	binance_api_key = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))
	binance_api_secret = forms.CharField(max_length=200, widget=forms.TextInput(
									attrs={'class':'form-control'}))

								




