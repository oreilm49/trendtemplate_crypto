from typing import Optional, Sequence

from binance.client import Client
import pandas as pd

from constants import PRICE_DATA_COLUMNS, BASE_CURRENCIES
from exceptions import InvalidTicker, DowntrendingException


class Ticker:
    price_data: Optional[pd.DataFrame] = None

    def __init__(self, symbol: str, client: Optional[Client] = None,
                 valid_base_currencies: Sequence[str] = BASE_CURRENCIES) -> None:
        super().__init__()
        self.symbol = symbol
        self.client = client
        self.valid_base_currencies = valid_base_currencies
        self.base_currency, self.coin = self.get_base_currency_and_coin(symbol)

    def __str__(self) -> str:
        return self.symbol

    def get_year_price_data(self) -> pd.DataFrame:
        if self.price_data is None:
            self.price_data = self._get_year_price_data()
        return self.price_data

    def _get_year_price_data(self) -> pd.DataFrame:
        assert self.client is not None, "You forgot to pass a client"
        candles = self.client.get_historical_klines(self.symbol, Client.KLINE_INTERVAL_1DAY, "1 year ago UTC")
        price_data: pd.DataFrame = pd.DataFrame(candles, columns=PRICE_DATA_COLUMNS.keys())\
            .astype(PRICE_DATA_COLUMNS)
        price_data['time_open'] = price_data['time_open'].apply(pd.Timestamp, unit="ms")
        price_data['time_close'] = price_data['time_close'].apply(pd.Timestamp, unit="ms")
        price_data['50MA'] = price_data['close'].rolling(window=50).mean()
        price_data['150MA'] = price_data['close'].rolling(window=150).mean()
        price_data['200MA'] = price_data['close'].rolling(window=200).mean()
        return price_data

    def in_uptrend(self) -> bool:
        price_data: pd.DataFrame = self.get_year_price_data()
        yearly_high = price_data['high'].max()
        yearly_low = price_data['low'].min()
        close = price_data['close'].iloc[-1]
        fifty_day = price_data['50MA'].iloc[-1]
        one_fifty_day = price_data['150MA'].iloc[-1]
        two_hundred_day = price_data['200MA'].iloc[-1]
        try:
            if not close > fifty_day:
                raise DowntrendingException(f"{self.symbol} closed below 50 day. Close: {close}. 50 day: {fifty_day}")
            if not close > one_fifty_day:
                raise DowntrendingException(
                    f"{self.symbol} closed below 150 day. Close: {close}. 150 day: {one_fifty_day}")
            if not close > two_hundred_day:
                raise DowntrendingException(
                    f"{self.symbol} closed below 200 day. Close: {close}. 200 day: {two_hundred_day}")
            if not one_fifty_day > two_hundred_day:
                raise DowntrendingException(
                    f"{self.symbol} 150 day is below 200 day. 150 day: {one_fifty_day}. 200 day: {two_hundred_day}")
            two_hundred_day_is_monotonic: bool = price_data['200MA'].iloc[-1:-30].is_monotonic
            if not two_hundred_day_is_monotonic:
                raise DowntrendingException(
                    f"{self.symbol} 200 day is not monotonic (in an uptrend): 200 day: {two_hundred_day}. 30 days ago: {price_data['200MA'].iloc[-30]}")
            if not fifty_day > one_fifty_day:
                raise DowntrendingException(
                    f"{self.symbol} 50 day is below 150 day. 50 day: {fifty_day}. 150 day: {one_fifty_day}")
            if not fifty_day > two_hundred_day:
                raise DowntrendingException(
                    f"{self.symbol} 50 day is below 200 day. 50 day: {fifty_day}. 200 day: {two_hundred_day}")
            if not ((close - yearly_low) / close) > 0.30:
                raise DowntrendingException(
                    f"{self.symbol} Close is less than 30% above its 52-week low. Close: {close}. 52 week low: {yearly_low}")
            if not ((close - yearly_high) / close) > -0.25:
                raise DowntrendingException(
                    f"{self.symbol} Close is not within at 25% of its 52-week high. Close: {close}. 52 week low: {yearly_low}")
        except DowntrendingException as e:
            return False
        return True

    def get_base_currency_and_coin(self, ticker: str) -> tuple[str, str]:
        slice_sizes = 3, 4
        for size in slice_sizes:
            base_currency = ticker[-size:]
            coin = ticker[:-size]
            if base_currency in self.valid_base_currencies:
                return base_currency, coin
        raise InvalidTicker(f"{ticker} doesn't seem to have a valid base currency.")
