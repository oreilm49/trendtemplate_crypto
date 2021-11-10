API_URL = "https://api.binance.com"
BASE_CURRENCY_BUSD = "BUSD"
BASE_CURRENCY_USDT = "USDT"
BASE_CURRENCY_USDC = "USDC"
BASE_CURRENCY_DAI = "DAI"
BASE_CURRENCY_TUSD = "TUSD"
BASE_CURRENCY_BTC = "BTC"
BASE_CURRENCY_ETH = "ETH"
BASE_CURRENCIES = (BASE_CURRENCY_BUSD, BASE_CURRENCY_USDT, BASE_CURRENCY_USDC, BASE_CURRENCY_DAI, BASE_CURRENCY_TUSD,
                   BASE_CURRENCY_BTC, BASE_CURRENCY_ETH,
                   )
PRICE_DATA_COLUMNS = {
    'time_open': "O",
    'open': "f",
    'high': "f",
    'low': "f",
    'Close': "f",
    'volume': "f",
    'time_close': "O",
    'quote_asset_volume': "f",
    'number_of_trades': "f",
    'taker_buy_base_asset_volume': "f",
    'taker_buy_quote_asset_volume': "f",
    'to_be_ignored': "f"
}
STOCK_INFO_52_WEEK_HIGH = "fiftyTwoWeekHigh"
STOCK_INFO_52_WEEK_LOW = "fiftyTwoWeekLow"
STOCK_INFO_PREV_CLOSE = "previousClose"
