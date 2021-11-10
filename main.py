import argparse
from typing import Optional, Sequence

from constants import BASE_CURRENCIES, BASE_CURRENCIES_USD_PEG
from exceptions import InvalidBaseCurrency, DuplicatedArgs
from exchanges import Binance

parser = argparse.ArgumentParser(
    prog="Trend template - crypto",
)
parser.add_argument('-bc', '--base_currencies', nargs='+', help='One or more base currencies to use to screen coins.')
parser.add_argument('-usd', '--usd_pairs', help='Only screen USD pairs.', action='store_true')
parser.set_defaults(usd_pairs=False)


if __name__ == '__main__':
    args = parser.parse_args()
    base_currencies: Optional[list[str]] = args.base_currencies
    usd_pairs: bool = args.usd_pairs
    valid_base_currencies: Optional[Sequence[str]] = None
    if base_currencies and usd_pairs:
        raise DuplicatedArgs("You can't specify both base_currencies and usd_pairs")
    if base_currencies:
        for currency in base_currencies:
            if currency not in BASE_CURRENCIES:
                raise InvalidBaseCurrency(f"Invalid base currency: {currency}. Must be one of: {','.join(BASE_CURRENCIES)}")
        valid_base_currencies = base_currencies
    elif usd_pairs:
        valid_base_currencies = BASE_CURRENCIES_USD_PEG
    for ticker in Binance(valid_base_currencies=valid_base_currencies).uptrending_stocks():
        print(ticker)
