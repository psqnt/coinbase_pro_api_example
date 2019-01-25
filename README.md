## Coinbase Pro API example
Using [coinbasepro-python](https://github.com/danpaquin/coinbasepro-python) Public Client

This gets 24 hour data from coinbase pro api and displays it on a webpage.

code connecting to API is located in management/commands directory, the data is
added to the Django models and saved to the database.


## updating database
I set up a cron job to run every 10 minutes.

```
crontab -e
*/10 * * * * path/to/python3 path/to/manage.py update_marketdata
```

Mine looks like this
`*/10 * * * * /usr/local/bin/python3 /Users/Joe/Projects/develop/coinbase/price_server/crypto/manage.py update_marketdata`
