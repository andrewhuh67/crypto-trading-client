# from background_task import background
# from cryptoclient.models import UserAddresses
# from cryptoclient.wrapper_binance import BinanceAPI
# from cryptoclient.wrapper_binance2 import Binance2Auth
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# import datetime
# import time
# from background_task.tasks import tasks, autodiscover

# @background(schedule=0)
# def save_address(user_id):


# 	binance2 = Binance2Auth()

# 	crypto_list = binance2.every_crypto_binance()

# 	# obj = get_object_or_404(User, pk=user_id)

# 	main_cryptos = ['BTC', 'ETH', 'LTC']

# 	obj = User.objects.get(pk=user_id)

# 	for item in main_cryptos:
# 		address = binance2.get_deposit_address(item)
# 		user_address = UserAddresses()
		
# 		if address['success'] == False:
# 			continue

# 		elif UserAddresses.objects.filter(crypto=item,user=obj).first() == None:
# 			user_address.crypto = item
# 			user_address.address = address['address']
# 			user_address.user = obj
# 			user_address.save()
# 			print('Worked')
		
# 		else:
# 			continue

# 		time.sleep(2)

# 	for item in crypto_list:
# 		if item in main_cryptos:
# 			continue

# 		else:
# 			address = binance2.get_deposit_address(item)
# 			# print(item, type(address), address)
# 			user_address = UserAddresses()
# 			if address['success'] == False:
# 				continue

# 			elif UserAddresses.objects.filter(crypto=item,user=obj).first() == None:
# 				print(address)
				

# 				print(item, address['address'], len(address['address']))
# 				user_address.crypto = item
# 				user_address.address = address['address']
# 				user_address.user = obj
# 				user_address.save()
# 				print('Other Addresses')
			

# 			else:
					
# 				continue

# 		time.sleep(2)

    # lookup user by id and send them a message

    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')