from binance.client import Client
import pandas as pd

from constants import PRICE_DATA_COLUMNS


class DowntrendingException(Exception):
    pass


class Ticker:
    def __init__(self, ticker: str, client: Client) -> None:
        super().__init__()
        self.ticker = ticker
        self.client = client
        self.price_data = self.get_year_price_data()
        self.info = self._get_info()

    def _get_info(self):
        return {
            'fiftyTwoWeekHigh': self.price_data['high'].max(),
            'fiftyTwoWeekLow': self.price_data['low'].min(),
            'previousClose': self.price_data['Close'].iloc[-1],
        }

    def get_year_price_data(self) -> pd.DataFrame:
        candles = self.client.get_historical_klines(self.ticker, Client.KLINE_INTERVAL_1DAY, "1 year ago UTC")
        price_data: pd.DataFrame = pd.DataFrame(candles, columns=PRICE_DATA_COLUMNS.keys())\
            .astype(PRICE_DATA_COLUMNS)
        price_data['time_open'] = price_data['time_open'].apply(pd.Timestamp, unit="ms")
        price_data['time_close'] = price_data['time_close'].apply(pd.Timestamp, unit="ms")
        price_data['50MA'] = price_data['Close'].rolling(window=50).mean()
        price_data['150MA'] = price_data['Close'].rolling(window=150).mean()
        price_data['200MA'] = price_data['Close'].rolling(window=200).mean()
        return price_data

    def in_uptrend(self) -> bool:
        yearly_high = self.info["fiftyTwoWeekHigh"]
        yearly_low = self.info["fiftyTwoWeekLow"]
        close = self.info["previousClose"]
        fifty_day = self.price_data['50MA'].iloc[-1]
        one_fifty_day = self.price_data['150MA'].iloc[-1]
        two_hundred_day = self.price_data['200MA'].iloc[-1]
        try:
            if not close > fifty_day:
                raise DowntrendingException(f"{self.ticker} closed below 50 day. Close: {close}. 50 day: {fifty_day}")
            if not close > one_fifty_day:
                raise DowntrendingException(
                    f"{self.ticker} closed below 150 day. Close: {close}. 150 day: {one_fifty_day}")
            if not close > two_hundred_day:
                raise DowntrendingException(
                    f"{self.ticker} closed below 200 day. Close: {close}. 200 day: {two_hundred_day}")
            if not one_fifty_day > two_hundred_day:
                raise DowntrendingException(
                    f"{self.ticker} 150 day is below 200 day. 150 day: {one_fifty_day}. 200 day: {two_hundred_day}")
            two_hundred_day_is_monotonic: bool = self.price_data['200MA'].iloc[-1:-30].is_monotonic
            if not two_hundred_day_is_monotonic:
                raise DowntrendingException(
                    f"{self.ticker} 200 day is not monotonic (in an uptrend): 200 day: {two_hundred_day}. 30 days ago: {self.price_data['200MA'].iloc[-30]}")
            if not fifty_day > one_fifty_day:
                raise DowntrendingException(
                    f"{self.ticker} 50 day is below 150 day. 50 day: {fifty_day}. 150 day: {one_fifty_day}")
            if not fifty_day > two_hundred_day:
                raise DowntrendingException(
                    f"{self.ticker} 50 day is below 200 day. 50 day: {fifty_day}. 200 day: {two_hundred_day}")
            if not ((close - yearly_low) / close) > 0.30:
                raise DowntrendingException(
                    f"{self.ticker} Close is less than 30% above its 52-week low. Close: {close}. 52 week low: {yearly_low}")
            if not ((close - yearly_high) / close) > -0.25:
                raise DowntrendingException(
                    f"{self.ticker} Close is not within at 25% of its 52-week high. Close: {close}. 52 week low: {yearly_low}")
        except DowntrendingException as e:
            return False
        return True
