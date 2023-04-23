import http.server
import json
import urllib.parse
import requests

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


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        query_dict = urllib.parse.parse_qs(query)

        if path == "/get_average_exchange_rate":
            date = query_dict.get("date", [None])[0]
            currency_code = query_dict.get("currency_code", [None])[0]
            data = resp_connector_to_nbp_api("a", currency_code, date=date)
            if data and data.get("rates"):
                avg_rate = data["rates"][0].get("mid", None)
                if avg_rate:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps({"average_exchange_rate": avg_rate}).encode()
                    )
                    return
            self.send_error(500, "Error fetching exchange rate data")

        elif path == "/get_max_min_average_value":
            currency_code = query_dict.get("currency_code", [None])[0]
            n = query_dict.get("n", [None])[0]
            if n is not None:
                n = int(n)
            data = resp_connector_to_nbp_api("a", currency_code, n=n)
            if data and data.get("rates"):
                rates = data["rates"]
                if len(rates) >= n:
                    avg_rates = [rate["mid"] for rate in rates]
                    max_rate = max(avg_rates)
                    min_rate = min(avg_rates)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps(
                            {
                                "max_average_value": max_rate,
                                "min_average_value": min_rate,
                            }
                        ).encode()
                    )
                    return
            self.send_error(
                500, f"Not enough data available for the last {n} quotations"
            )

        elif path == "/get_major_difference":
            currency_code = query_dict.get("currency_code", [None])[0]
            n = query_dict.get("n", [None])[0]
            if n is not None:
                n = int(n)
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
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps({"major_difference": major_difference}).encode()
                    )
                    return
            self.send_error(500, "Error fetching exchange rate data")

        else:
            self.send_error(404, "Not Found")


def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
