from django.shortcuts import render
from django.contrib import messages
import requests
from .forms import AverageExchangeRateForm, MaxMinAverageValueForm, MajorDifferenceForm


NBP_API_URL = "http://api.nbp.pl/api/exchangerates/rates"


def resp_connector_to_nbp_api(table, currency_code, date=None, n=None):
    try:
        url = f"{NBP_API_URL}/{table}/{currency_code}"
        if date is not None:
            url += f"/{date}"
        if n is not None:
            url += f"/last/{n}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"Error: {e}"
        if isinstance(e, requests.exceptions.HTTPError):
            error_msg = f"Error: {e.response.status_code} {e.response.reason}"
        return {"error": error_msg}
    except (IndexError, KeyError):
        return {"error": "Error fetching exchange rate data"}


def home(request):
    return render(request, "web/base.html")


def get_average_exchange_rate(request):
    if request.method == "POST":
        form = AverageExchangeRateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            currency_code = form.cleaned_data["currency_code"]
            data = resp_connector_to_nbp_api("a", currency_code, date=date)
            if data and data.get("rates"):
                avg_rate = data["rates"][0].get("mid", None)
                if avg_rate:
                    return render(
                        request,
                        "web/average_exchange_rate.html",
                        {
                            "average_exchange_rate": avg_rate,
                            "date": date,
                            "currency_code": currency_code,
                        },
                    )
            messages.error(request, "Error fetching exchange rate data")
    else:
        form = AverageExchangeRateForm()
    return render(request, "web/average_exchange_rate_form.html", {"form": form})


def get_max_min_average_value(request):
    if request.method == "POST":
        form = MaxMinAverageValueForm(request.POST)
        if form.is_valid():
            currency_code = form.cleaned_data["currency_code"]
            n = form.cleaned_data["n"]
            data = resp_connector_to_nbp_api("a", currency_code, n=n)
            if data and data.get("rates"):
                rates = data["rates"]
                if len(rates) >= n:
                    avg_rates = [rate["mid"] for rate in rates]
                    max_rate = max(avg_rates)
                    min_rate = min(avg_rates)
                    return render(
                        request,
                        "web/max_min_average_value.html",
                        {
                            "max_average_value": max_rate,
                            "min_average_value": min_rate,
                            "currency_code": currency_code,
                            "n": n,
                        },
                    )
            messages.error(
                request, f"Not enough data available for the last {n} quotations"
            )
        else:
            messages.error(request, "Error fetching exchange rate data")
    else:
        form = MaxMinAverageValueForm()
    return render(request, "web/max_min_average_value_form.html", {"form": form})


def get_major_difference(request):
    if request.method == "POST":
        form = MajorDifferenceForm(request.POST)
        if form.is_valid():
            currency_code = form.cleaned_data["currency_code"]
            n = form.cleaned_data["n"]
            data = resp_connector_to_nbp_api("c", currency_code, n=n)
            if data and "error" not in data:
                buy_rates = [rate["bid"] for rate in data["rates"]]
                sell_rates = [rate["ask"] for rate in data["rates"]]
                differences = [
                    abs(buy_rates[i] - sell_rates[i]) for i in range(len(buy_rates))
                ]
                major_difference = max(differences)
                rates = data["rates"]
                if buy_rates and sell_rates and len(rates) >= n:
                    return render(
                        request,
                        "web/major_difference.html",
                        {
                            "major_difference": major_difference,
                            "currency_code": currency_code,
                            "n": n,
                        },
                    )
                else:
                    return render(
                        request,
                        "web/error.html",
                        {
                            "error": f"Not enough data available for the last {n} quotations"
                        },
                    )
            else:
                return render(
                    request,
                    "web/error.html",
                    {"error": "Error fetching exchange rate data"},
                )
    else:
        form = MajorDifferenceForm()
    return render(request, "web/major_difference_form.html", {"form": form})
