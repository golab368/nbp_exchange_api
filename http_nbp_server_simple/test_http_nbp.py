import unittest
import http.client
import json


class TestNBPServer(unittest.TestCase):
    server_address = "localhost"
    server_port = 8000

    def test_get_average_exchange_rate(self):
        connection = http.client.HTTPConnection(self.server_address, self.server_port)
        connection.request(
            "GET", "/get_average_exchange_rate?currency_code=USD&date=2021-09-01"
        )
        response = connection.getresponse()
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())
        self.assertIn("average_exchange_rate", data)

    def test_get_max_min_average_value(self):
        connection = http.client.HTTPConnection(self.server_address, self.server_port)
        connection.request("GET", "/get_max_min_average_value?currency_code=USD&n=10")
        response = connection.getresponse()
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())
        self.assertIn("max_average_value", data)
        self.assertIn("min_average_value", data)

    def test_get_major_difference(self):
        connection = http.client.HTTPConnection(self.server_address, self.server_port)
        connection.request("GET", "/get_major_difference?currency_code=USD&n=10")
        response = connection.getresponse()
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())
        self.assertIn("major_difference", data)


if __name__ == "__main__":
    unittest.main()
