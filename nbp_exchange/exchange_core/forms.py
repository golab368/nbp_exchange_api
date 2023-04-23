import requests
from django import forms
from django.core.exceptions import ValidationError


class CurrencyChoiceField(forms.ChoiceField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.choices = self.get_currency_choices()

    def get_currency_choices(self):
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/a")
        if response.status_code == 200:
            currencies = response.json()[0]["rates"]
            return [(c["code"], c["code"]) for c in currencies]
        else:
            return [
                ("USD", "USD"),
                ("EUR", "EUR"),
                ("GBP", "GBP"),
                ("CHF", "CHF"),
                ("JPY", "JPY"),
            ]


class AverageExchangeRateForm(forms.Form):
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={"type": "date"}))
    currency_code = currency_code = CurrencyChoiceField(label="Currency Code")

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        currency_code = cleaned_data.get("currency_code")
        url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/{date}/?format=json"

        response = requests.get(url)
        if response.status_code != 200:
            raise ValidationError(
                "There is no data available for the selected date and currency code. Please choose another date or currency."
            )


class MaxMinAverageValueForm(forms.Form):
    currency_code = CurrencyChoiceField(label="Currency Code")
    n = forms.IntegerField(
        label="Number of Last Quotations", min_value=1, max_value=255
    )


class MajorDifferenceForm(forms.Form):
    currency_code = CurrencyChoiceField(label="Currency Code")
    n = forms.IntegerField(
        label="Number of Last Quotations", min_value=1, max_value=255
    )
