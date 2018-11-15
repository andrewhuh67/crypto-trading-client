from django.db import models
from django.utils import timezone
from project.settings import AUTH_USER_MODEL

# Create your models here.

class PastBuySell(models.Model):

	# order_type = buy or sell
	# asset_class = example = BTC/USD
	# dollar amount
	
	order_type = models.CharField(max_length=5)
	asset_class = models.CharField(max_length=10)
	last_price = models.CharField(max_length=20)
	trade_volume = models.CharField(max_length=20)
	timestamp = models.DateTimeField(default=timezone.now)


class PastSwaps(models.Model):
	
	crypto_pair = models.CharField(max_length=10)
	last_price = models.CharField(max_length=10)
	amount_of_crypto_spent = models.CharField(max_length=20)
	amount_of_crypto_received = models.CharField(max_length=20)
	timestamp = models.DateTimeField(default=timezone.now)

class UserAddresses(models.Model):
	crypto = models.CharField(max_length=10)
	address = models.CharField(max_length=150)
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)

class UserCredentials(models.Model):
	cb_api_key = models.CharField(max_length=200)
	cb_secret_key = models.CharField(max_length=200)
	gdax_api_key = models.CharField(max_length=200)
	gdax_secret_key = models.CharField(max_length=200)
	gdax_passphrase = models.CharField(max_length=200)
	coinigy_api_key = models.CharField(max_length=200)
	coinigy_api_secret = models.CharField(max_length=200)
	binance_api_key = models.CharField(max_length=200)
	binance_api_secret = models.CharField(max_length=200)
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)

class UserBinanceOrders(models.Model):
	crypto_pair = models.CharField(max_length=10)
	order_type = models.CharField(max_length=10)
	buy_or_sell = models.CharField(max_length=5)
	price = models.FloatField()
	amount = models.FloatField()
	timestamp = models.DateTimeField(default=timezone.now)
	exchange = models.CharField(max_length=10, default='Binance')
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)


class UserGdaxOrders(models.Model):
	crypto_pair = models.CharField(max_length=10)
	order_type = models.CharField(max_length=10)
	buy_or_sell = models.CharField(max_length=5)
	price = models.FloatField()
	amount = models.FloatField()
	timestamp = models.DateTimeField(default=timezone.now)
	exchange = models.CharField(max_length=10, default='GDAX')
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)










