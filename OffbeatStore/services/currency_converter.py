import requests
from OffbeatStore import cache


class ExchangeRateClient:
    BASE_URL = "http://api.exchangerate.host"
    LATEST_ENDPOINT = "/latest"

    def __init__(self, api_key):
        self.api_key = api_key

    def __request_data(self):
        url = f"{self.BASE_URL}{self.LATEST_ENDPOINT}?access_key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        return data["rates"]

    @cache.cached(timeout=3600, key_prefix="__get_data")
    def __get_data(self):
        data = self.__request_data()
        return data

    def convert_price(self, value: int, currency: str) -> int:
        conversion_data = self.__get_data()
        return value * conversion_data.get(currency, 1)
