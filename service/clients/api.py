
import os

from service.clients.countries import CountryClient


class ApiClient:
    def __init__(self, url: str) -> None:
        self.url = url
        self.countries = CountryClient(url)


client = ApiClient(os.environ['API_URL'])
