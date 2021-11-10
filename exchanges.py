import json
from collections import Iterator, Sequence
from binance.client import Client

from constants import BASE_CURRENCIES_USD_PEG, BASE_CURRENCIES
from exceptions import InvalidTicker
from ticker import Ticker


class Binance:
    def __init__(self, valid_base_currencies: Sequence[str] = BASE_CURRENCIES) -> None:
        super().__init__()
        self.client: Client = self.conn()
        self.valid_base_currencies = valid_base_currencies

    def conn(self) -> Client:
        with open("config.json", "r") as read_file:
            config = json.load(read_file)
            return Client(config['api_key'], config['api_secret'])

    def valid_tickers(self) -> Iterator[Ticker]:
        """"""
        tickers = self.client.get_all_tickers()
        for ticker in sorted(tickers, key=lambda d: d['symbol']):
            try:
                yield Ticker(ticker['symbol'], client=self.client, valid_base_currencies=self.valid_base_currencies)
            except InvalidTicker:
                pass

    def uptrending_stocks(self) -> Iterator[str]:
        peg_trending: list[str] = []
        for ticker in self.valid_tickers():
            # avoid checking the same coin twice, just because the base pair is different
            if ticker.coin in peg_trending:
                continue
            try:
                if ticker.in_uptrend():
                    if ticker.base_currency in BASE_CURRENCIES_USD_PEG:
                        peg_trending.append(ticker.coin)
                    yield ticker
            except IndexError:
                pass
            except Exception as e:
                print(f"error: {ticker.symbol} - {e}")
