from exchanges import Binance

if __name__ == '__main__':
    for ticker in Binance().uptrending_stocks():
        print(ticker)
