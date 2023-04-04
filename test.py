import yfinance as yf
import pandas as pd
import mplfinance as mpf

#First test with python ya dig

def basic_trendline(df):
    high_p = df["High"]
    # Grab peaks






def crypto_candles():
    dataF = yf.download("BTC-USD", start="2020-5-1", end="2023-4-4", interval='1d')
    
    print(dataF["High"])

    mpf.plot(dataF, type='candle', style ='charles', title='BTC', ylabel=f'Price in USD')

    return dataF


crypto_candles()