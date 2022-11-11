import httpx

from service.clients.schemas import Country, Visa


class CountryClient:
    def __init__(self, url: str) -> None:
        self.url = f'{url}/countries'

    def get_all(self) -> list[Country]:
        response = httpx.get(url=f'{self.url}/')
        response.raise_for_status()
        countries = response.json()
        return [Country(**country) for country in countries]

    def get_visas(self, country: int) -> list[Visa]:
        response = httpx.get(url=f'{self.url}/{country}/visas/')
        response.raise_for_status()
        visas = response.json()
        return [Visa(**visa) for visa in visas]
