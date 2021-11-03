import json
from collections import Iterator

from binance.client import Client
import pandas as pd

from constants import BASE_CURRENCY_BUSD, PRICE_DATA_COLUMNS


class Binance:
    def __init__(self) -> None:
        super().__init__()
        self.client = self.conn()

    def conn(self) -> Client:
        with open("config.json", "r") as read_file:
            config = json.load(read_file)
            return Client(config['api_key'], config['api_secret'])

    def busd_tickers(self) -> Iterator[str]:
        tickers = self.client.get_all_tickers()
        for ticker in tickers:
            if ticker['symbol'][-4:] == BASE_CURRENCY_BUSD:
                yield ticker['symbol']

    def get_year_price_data(self, symbol: str):
        candles = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 year ago UTC")
        price_data: pd.DataFrame = pd.DataFrame(candles, columns=PRICE_DATA_COLUMNS.keys())\
            .astype(PRICE_DATA_COLUMNS)
        price_data['time_open'] = price_data['time_open'].apply(pd.Timestamp, unit="ms")
        price_data['time_close'] = price_data['time_close'].apply(pd.Timestamp, unit="ms")
        price_data['50MA'] = price_data['Close'].rolling(window=50).mean()
        price_data['150MA'] = price_data['Close'].rolling(window=150).mean()
        price_data['200MA'] = price_data['Close'].rolling(window=200).mean()
        return price_data


class Ticker:
    def __init__(self, symbol: str, price_data: pd.DataFrame) -> None:
        assert len(price_data) == 365, "price data must be for a full year"
        super().__init__()
        self.symbol = symbol
        self.price_data = price_data
        self.info = self._get_info()

    def _get_info(self):
        return {
            'fiftyTwoWeekHigh': self.price_data['high'].max(),
            'fiftyTwoWeekLow': self.price_data['low'].min(),
            'previousClose': self.price_data['Close'].iloc[-1],
        }


if __name__ == '__main__':
    pass
