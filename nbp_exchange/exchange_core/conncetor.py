import requests
from datetime import date, timedelta
from .models import ExchangeRate

def populate_exchange_rates():
    currencies = ['USD', 'EUR', 'GBP', 'CHF']
    start_date = date(2020, 1, 1)
    end_date = date.today() - timedelta(days=1)

    for currency in currencies:
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:
                url = f"http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{current_date}/"
                response = requests.get(url)
                if response:
                    data = response.json()
                    if len(data["rates"]) > 0:
                        rate_data = data["rates"][0]
                        exchange_rate = ExchangeRate(currency=currency, date=current_date,
                                                    average_rate=rate_data["mid"],
                                                    buy_rate=rate_data["bid"],
                                                    sell_rate=rate_data["ask"])
                        exchange_rate.save()
                current_date += timedelta(days=1)
