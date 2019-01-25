"""
Run this to get all initial data loaded into database.
"""

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from marketdata.models import Currency, Product

from cbpro import PublicClient

def load_currencies():
    """
    Load currencies into database that are on the coinbase pro exchange.

    first check if they are in the database before adding them.
    """
    currency_list = Currency.objects.all() # currencies already added
    client = PublicClient() # connect client to coinbase pro
    coinbase_currency_list = client.get_currencies() # get currency list

    added_count = 0
    for currency in coinbase_currency_list:
        if currency['details']['type'] == 'crypto': # only add crytos
            pass # I think I will add all of them now. fuck it.
        c, created = Currency.objects.get_or_create(
                        symbol=currency['id'],
                        name=currency['name']
                    )
        c.save()
        if created:
            added_count += 1

    return added_count


def load_products():
    """
    Load products into database that are on the coinbase pro exchange.

    only add if they are not already in database.
    """
    product_list = Product.objects.all()
    client = PublicClient()
    coinbase_product_list = client.get_products()

    added_count = 0
    for product in coinbase_product_list:
        base = Currency.objects.get(symbol=product['base_currency'])
        quote = Currency.objects.get(symbol=product['quote_currency'])
        p, created = Product.objects.get_or_create(
                        product_id=product['id'],
                        base_currency=base,
                        quote_currency=quote,
                        display_name=product['display_name']
                    )
        p.save()
        if created:
            added_count += 1

    return added_count

class Command(BaseCommand):
    help = "Loads initial data into database from coinbase"

    def handle(self, *args, **kwargs):
        currencies_loaded = load_currencies()
        products_loaded = load_products()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded in {currencies_loaded} currencies.\n'+
                f'Successfully loaded in {products_loaded} products.'
            )
        )
