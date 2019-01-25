"""
Provides functionality for updating market data from coinbase pro.

24 hour statistics.

Will need to add this to a crontab something like this:

python manage.py update_marketdata.py
"""
from time import sleep
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from marketdata.models import Product, ProductStatistics

from cbpro import PublicClient

from decimal import Decimal

def insert_product_stats(id, stats):
    """
    Insert new row of product statistics into database.
    """
    print(f'Inserting {id} with {stats}')
    open=float(stats['open'])
    high=float(stats['high'])
    low=float(stats['low'])
    volume=float(stats['volume'])
    last=float(stats['last'])
    volume_30day=float(stats['volume_30day'])

    #print(typeof(open))
    ps = ProductStatistics(
            product=id,
            open=open,
            high=high,
            low=low,
            volume=volume,
            last=last,
            volume_30day=volume_30day
        )
    ps.save()


def update_24hour_statistics():
    """
    Loads the 24 hour market data statistics from coinbase pro
    into our database.
    """
    client = PublicClient()

    products = Product.objects.all()

    stats_list = []
    for product in products:
        s = client.get_product_24hr_stats(product.product_id)
        if 'message' in s:
            print(f'API rate limit exceeded with {product.product_id}. retrying in 10')
            sleep(10)
            s = client.get_product_24hr_stats(product.product_id)
            if 'message' in s:
                continue
        print(f'Packaging {product} with marketdata.')
        package = [product, s]
        stats_list.append(package)
        sleep(1)

    added_count = 0
    print('Inserting producted data to database.')
    for s in stats_list:
        insert_product_stats(s[0], s[1])
        added_count += 1

    return added_count


class Command(BaseCommand):
    help = "Inserts now row of market data for each product"

    def handle(self, *args, **kwargs):
        added_count = update_24hour_statistics()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully inserted {added_count} rows of 24hr market data.'
            )
        )
