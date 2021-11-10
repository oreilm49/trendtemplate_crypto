import json
from collections import Iterator
from binance.client import Client

from constants import BASE_CURRENCIES
from ticker import Ticker


class Binance:
    def __init__(self) -> None:
        super().__init__()
        self.client: Client = self.conn()

    def conn(self) -> Client:
        with open("config.json", "r") as read_file:
            config = json.load(read_file)
            return Client(config['api_key'], config['api_secret'])

    def valid_tickers(self) -> Iterator[str]:
        tickers = self.client.get_all_tickers()
        for ticker in tickers:
            if ticker['symbol'][-4:] in BASE_CURRENCIES:
                yield ticker['symbol']

    def uptrending_stocks(self) -> Iterator[str]:
        for symbol in self.valid_tickers():
            try:
                ticker = Ticker(symbol, self.client)
                if ticker.in_uptrend():
                    yield symbol
            except IndexError:
                pass
            except Exception as e:
                print(f"error: {symbol} - {e}")
