from django.db import models
from django.utils import timezone

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
