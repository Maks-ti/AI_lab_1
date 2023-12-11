import requests
import json

from requests import Response
from graph_definition import GraphNode

'''
url = "http://api.currencylayer.com/list"
params = {
    "access_key": "cbdaabe4b8f76243c6acc161a45cb9d3"
}

response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data, indent=4))

'''

'''
url = "http://apilayer.net/api/live"
params = {
    "access_key": "cbdaabe4b8f76243c6acc161a45cb9d3",
    "source": "EUR"
}

response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data, indent=4))

'''

DEBUG = True


# класс парсинга курсов и построения на лету графа данных курсов
class Parser:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Parser, cls).__new__(cls)
        return cls._instance

    def __init__(self, access_key: str):
        self.access_key = access_key
        self.currencies: dict[str, str] | None = None
        self.all_quotes: dict[str, float] = dict()
        self.all_quotes_got: bool = False
        self.node_pool: dict[str, GraphNode] = dict()

    def __create_node_pool(self):
        print('creating all vertexes')
        # создание узлов графа для каждой валюты
        for currency in self.currencies:
            self.node_pool[currency] = GraphNode(currency, [])
        print('all vertexes created')
        return

    def __create_edges(self):
        print('creating all edges')
        for key in self.all_quotes:
            node_from_name: str = key[:3]
            node_to_name: str = key[3:]

            if node_from_name not in self.node_pool or node_to_name not in self.node_pool:
                # связь есть - вершин таких нет (скипаем связь)
                continue

            node_from: GraphNode = self.node_pool[node_from_name]
            node_to: GraphNode = self.node_pool[node_to_name]
            node_from.children.append(node_to)
        print('all edges created')
        return

    def __get_all_currencies(self):
        global DEBUG
        if DEBUG:
            self.currencies = {
                "AED": "United Arab Emirates Dirham",
                "ANG": "Netherlands Antillean Guilder",
                "AUD": "Australian Dollar",
                "BRL": "Brazilian Real",
                "BTC": "Bitcoin",
                "CAD": "Canadian Dollar",
                "CLP": "Chilean Peso",
                "CNY": "Chinese Yuan",
                "EUR": "Euro",
                "GBP": "British Pound Sterling",
                "ILS": "Israeli New Sheqel",
                "INR": "Indian Rupee",
                "JPY": "Japanese Yen",
                "KPW": "North Korean Won",
                "KRW": "South Korean Won",
                "KZT": "Kazakhstani Tenge",
                "NOK": "Norwegian Krone",
                "PLN": "Polish Zloty",
                "RUB": "Russian Ruble",
                "TRY": "Turkish Lira",
                "USD": "United States Dollar",
                "XAU": "Gold (troy ounce)"
            }
            self.__create_node_pool()
            print(json.dumps(self.currencies, indent=4))
        else:
            url = "http://api.currencylayer.com/list"
            params = {
                "access_key": self.access_key
            }
            response: Response = requests.get(url, params=params)
            data = response.json()

            if data['success']:
                self.currencies = data['currencies']
                self.__create_node_pool()
            print(json.dumps(data, indent=4))
        return

    def __get_quotes_by_currency(self, name: str):
        url = "http://apilayer.net/api/live"
        params = {
            "access_key": self.access_key,
            "source": name
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data['success']:
            quotes: dict[str, float] = data['quotes']
            self.all_quotes.update(quotes)
        print(json.dumps(data, indent=4))
        return

    def get_all_quotes(self) -> dict:
        self.__get_all_currencies()
        for currency in self.currencies:  # key in dict
            self.__get_quotes_by_currency(currency)

        self.all_quotes_got = True
        self.__create_edges()
        return self.all_quotes



