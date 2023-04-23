from django.test import TestCase, Client
from django.urls import reverse
from exchange_core.forms import (
    AverageExchangeRateForm,
    MaxMinAverageValueForm,
    MajorDifferenceForm,
)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/base.html")

    def test_get_average_exchange_rate_view(self):
        form_data = {"currency_code": "USD", "date": "2023-04-20"}
        response = self.client.post(reverse("average_exchange_rate"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/average_exchange_rate.html")

    def test_get_max_min_average_value_view(self):
        form_data = {"currency_code": "USD", "n": 30}
        response = self.client.post(reverse("max_min_average_value"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/max_min_average_value.html")

    def test_get_major_difference_view(self):
        form_data = {"currency_code": "USD", "n": 30}
        response = self.client.post(reverse("major_difference"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/major_difference.html")

    def test_invalid_average_exchange_rate_form(self):
        form_data = {"currency_code": "USD", "date": "invalid_date"}
        response = self.client.post(reverse("average_exchange_rate"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/average_exchange_rate_form.html")
        self.assertIsInstance(response.context["form"], AverageExchangeRateForm)
        self.assertFormError(response, "form", "date", "Enter a valid date.")

    def test_invalid_max_min_average_value_form(self):
        form_data = {"currency_code": "USD", "n": "invalid_n"}
        response = self.client.post(reverse("max_min_average_value"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/max_min_average_value_form.html")
        self.assertIsInstance(response.context["form"], MaxMinAverageValueForm)
        self.assertFormError(response, "form", "n", "Enter a whole number.")

    def test_invalid_major_difference_form(self):
        form_data = {"currency_code": "USD", "n": "invalid_n"}
        response = self.client.post(reverse("major_difference"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/major_difference_form.html")
        self.assertIsInstance(response.context["form"], MajorDifferenceForm)
        self.assertFormError(response, "form", "n", "Enter a whole number.")
