import requests
from OffbeatStore import cache


class ExchangeRateClient:
    URL = "https://api.exchangerate.host/latest"

    def __request_data(self):
        response = requests.get(self.URL)
        data = response.json()
        return data["rates"]

    @cache.cached(timeout=3600, key_prefix="__get_data")
    def __get_data(self):
        data = self.__request_data()
        return data

    def convert_price(self, value: int, currency: str) -> int:
        conversion_data = self.__get_data()
        return value * conversion_data.get(currency, 1)
