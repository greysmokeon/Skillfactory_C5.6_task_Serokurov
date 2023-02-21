import requests
import json
from config import currencies


class ConvertionException(Exception):
    pass


class CryptoConvertor:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество валюты {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currencies[base]]
        total_base = total_base * amount

        return total_base
