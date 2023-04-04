import yfinance as yf
import pandas as pd
import mplfinance as mpf
import requests

#First test with python ya dig

def crypto_candles():
    dataF = yf.download("BTC-USD", start="2023-3-27", end="2023-4-3", interval='1h')
    dataF.iloc[:,:]
    dataF.Open.iloc

    mpf.plot(dataF, type='candle', style ='charles', title='BTC', ylabel=f'Price in USD')
    mpf.make_addplot()

    return dataF


def print_Excel(data):
    excel_file = "output.xlsx"
    sheet_name = "Data Set"
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    data.to_excel(writer, sheet_name=sheet_name)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    chart = workbook.add_chart({})


print_Excel(crypto_candles())