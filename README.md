# crypto-trading-client



APIs used: Coinbase Wallet API, GDAX, Coinigy

This application takes the secret keys and secret api keys from coinbase, GDAX, and binance in order to allow users to trade the main cryptocurrencies(bitcoin, ethereum, litecoin) and altcoins on the same platform. 

In order to use this application, you need to do a couple of things.

1. you need api keys from coinbase, gdax, coinigy, and binance (need to make accounts with all four)
2. need to connect your binance account to coinigy
3. need a credentials.py file in the cryptoclient application folder in order to have access to the accounts. There is a markdown file of what the credentials file is suppose to look. Copy the template over and make sure the keys are in strings.
4. in order to make requests to coinbase, the unix time on your computer has to be within 30 seconds of that of coinbase. Simpliest way of changing it is to change the time on your computer. The time on your computer should match up to the time coinbase is operating on. (Pacific Standard Time)

Git clone the application 

virtualenv env 

source env/bin/activate

pip install -r requirements.txt

go create credentials.py and copy the template of the credentials.py and put your api information as strings

go make a local_settings.py and submit a secret key as a string.

then go to the folder with manage.py and do python3 manage.py runserver


