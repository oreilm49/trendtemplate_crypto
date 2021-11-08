# Trend Template
This is an adaptation (for the crypto market) of Mark Minervini's trend template as described in his book [Trade like a stock market wizard](https://www.goodreads.com/en/book/show/16189528-trade-like-a-stock-market-wizard).

The sole purpose of this screener is to identify assets that are in a confirmed uptrend.

All [BUSD](https://www.binance.com/en/busd) pairs on Binance are screened to meet a specific criteria to confirm if the coin is in an uptrend.
This drastically reduces the noise in the market when searching for trading ideas.

## The criteria
* close > 50 day
* close > 150 day
* close > 200 day
* 150 day > 200 day
* 200 day is in an uptrend
* 50 day > 150 day
* 50 day > 200 day
* close is > 30% above 52 week low
* close within 25% of 52 week high

## Run in Python virtualenv
### Pre-requisites

* Python 3.9

### Set up the project
* `python3 -m venv`
* `source bin/activate`
* `pip install --upgrade pip`
* `pip install -r requirements.txt`
* Add a `config.json` to the project root containing your binance credentials:
    ```json
    {
        "api_key" : "<API_KEY>",
        "api_secret" : "<API_SECRET>"
    }
    ```

### Run the screener
* `./run.sh`
