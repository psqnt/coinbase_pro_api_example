import datetime
from django.db import models


class Currency(models.Model):
    """
    Model the 'currency' format from coinbase as thats where the data is
    coming from
    Example (Bitcoin):
    {
    'id': 'BTC',
    'name': 'Bitcoin',
    'min_size': '0.00000001',
    'status': 'online',
    'message': None,
    'details': {
        'type': 'crypto',
        'symbol': '₿',
        'network_confirmations': 6,
        'sort_order': 3,
        'crypto_address_link': 'https://live.blockcypher.com/btc/address/{{address}}',
        'crypto_transaction_link': 'https://live.blockcypher.com/btc/tx/{{txId}}',
        'push_payment_methods': ['crypto']
        }
    }

    This data only needs to be pulled once. (possibly pull once a week just to
    confirm nothing changes).
    """
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'({self.symbol}) {self.name}'


class Product(models.Model):
    """
    A product is the 'coinbase' product which is listing pairs.

    Ex. BTC-USD is the Bitcoin/US Dollar market
    """
    product_id = models.CharField(max_length=20)
    base_currency = models.ForeignKey(Currency, related_name='base_currency', on_delete=models.CASCADE)
    quote_currency = models.ForeignKey(Currency, related_name='quote_currency', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.display_name}'


class ProductStatistics(models.Model):
    """
    Hold 24hr statistics on a certain product

    Ex. (Bitcoin)
    {
        'open': '3581.26000000',
        'high': '3614.47000000',
        'low': '3530.84000000',
        'volume': '7802.85353667',
        'last': '3531.94000000',
        'volume_30day': '309826.47342979'
    }
    update this every 10 minutes???
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    last = models.FloatField()
    volume_30day = models.FloatField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} last updated: {self.last_updated}'
