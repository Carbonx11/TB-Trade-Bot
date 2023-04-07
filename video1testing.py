import yfinance as yf
import pandas as pd

#dataF = yf.download("EURUSD=X",start = "2020-1-1",end="2023-4-4",interval="1d")
#eurusd data between 2 dates on the 15m interval
#when trying to download data for low timeframes, yfinance only allows last 60 days

#print(dataF.iloc[:,:])#purely integer-location based indexing for seleciton by position
#dataF.Open.iloc#no idea what it does

#above data is used to test if signals and data is working not for live data



#2====define your signal function
#def signal_generator(df): #use your dataframe as a param cause when we are running
    #the live bot, we will acquire a dataframe and feed it to particular function
    #which returns a buy, sell or no clear signal
    
    #this example only detects engulfing candle patterns 
    #its an exmaple
 #   open = df.Open.iloc[-1]#read open price
  #  close = df.Close.iloc[-1]#read closing price of current candle or last candel of DF (-1)
   # previous_open = df.Open.iloc[-2]#open price of previous candle
    #previous_close = df.Close.iloc[-2]#close pricve of previous price
    
    #bearish pattern
    #if (open > close and previous_open < previous_close and close < previous_open
     #   and open >= previous_close):
      #  return 1
    #bullish pattern
    #elif (open<close and previous_open>previous_close and close > previous_open
     #     and open <= previous_close):
      #  return 2
    #else:
    #    return 0 #no clear pattern
    
    #test the function using the historical data
#signal = []
#signal.append(0)#append zero for first element of list so we dont have a signal at first
#for i in range(1,len(dataF)):#loop over all data in the dataframe (ALL THE ROW)
 #   df = dataF[i-1:i+1]#feed last 2 rows of the dataframe to make sure we use the correct set of data
  #  signal.append(signal_generator(df))#in each row we check if we have engulfing candle/append whatever function returns tolist
#dataF["signal"] = signal   #then we add this as a new column into the testing data dataframe
#print(dataF.iloc[:, :])
#print(dataF.signal.value_counts())#847 no signals, 1 buy and 1 sell signal in the presented data sets
    










print('\n\n===============\n\n')
import mplfinance as mpf
import pandas as pd
import requests


def crypto_candles(start_time,base_currency,vs_currency,interval):#1st param is when we start, 2 is providing what
    #we want to convert into 3 is vs which currency and 4 is interval of when do we want it?
    
    url = f'https://dev-api.shrimpy.io/v1/exchanges/binance/candles' #url where we get data
    
    #need some queries now
    payload = {'interval' : interval, 'baseTradingSymbol' : base_currency,
               'quoteTradingSymbol' : vs_currency, 'startTime' : start_time}
    
    response = requests.get(url,params=payload)
    data = response.json()
    
    #need a few lists to insert into the dataframe to get candles
    
    open_p,close_p,high_p,low_p,time_p,volume = [],[],[],[],[],[]
    #print(data) used to test it works
    for candle in data: #we want to append value at each index
        open_p.append(float(candle['open']))
        close_p.append(float(candle['close']))
        high_p.append(float(candle['high']))
        low_p.append(float(candle['low']))
        time_p.append(candle['time'])
        volume.append(float(candle['volume']))
    #now we create raw data to be cleaned with pandas
    raw_data = {
        'Date': pd.DatetimeIndex(time_p),
        'Open': open_p,
        'High': high_p,
        'Low': low_p,
        'Close': close_p,
        'Volume': volume
    }
    df = pd.DataFrame(raw_data).set_index('Date')#put the vars into a dataframe and set index to the date
    print(df)
    
    

    
    
    mpf.plot(df,type='candle',style='charles',title=base_currency,ylabel=f'Price in {vs_currency}'
             ,volume=True,mav=(9,15,50))
    #refer to plot lib, take in dataframe, type is candle, style charles makes the candles green and red
    #title is gonna be to base currency, and y label is gonna be the label describing the y plot
    mpf.show()
    
    #trend line rules:
    #draw a new trend line by connecting start of a trand with a valid swing point, and adjust as trade action 
    #unfolds
    
    return df #if you wanna use the info for further processin, its good to return df
                      
        
        
df =crypto_candles(start_time = '2022-12-15',base_currency = 'ETH', vs_currency='EUR',interval= '1d')

    
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

x = np.array([2, 7])
y = np.array([5, 15])
slope, intercept, r_value, p_value, std_err = linregress(x, y)
print("slope: %f, intercept: %f" % (slope, intercept))
print("R-squared: %f" % r_value**2)
#slope: 2.000000, intercept: 1.000000
#R-squared: 1.000000
  
plt.figure(figsize=(15, 5))
plt.plot(x, y, 'o', label='original data')
plt.plot(x, intercept + slope*x, 'r', label='fitted line')
plt.legend()
plt.grid()
plt.show()        
    
    
#process of drawing trend lines with dataframe
#1 Add 1 column for row numbering purpose for computation
#2 Compute at least 2 higher and lower data points in DataFrame
#3 Calculate a linear least-squares regression for trendlines
#4 Draw a close line and 2 trendlines by using matplotlib    

df['Number'] = np.arange(len(df)) + 1#add number for each row because index type is datetim and type is not 
#df['C'] = range(len(df))#appropriate for scipy.stats.linregres, so we added number column
print(df)

df_high = df.copy()
df_low = df.copy()
df.tail()
#code snippter how to pick up 2 high and lower data points from dataframe

#higher points returned
print('======')
while len(df_high)>2:
    slope, intercept, r_value, p_value, std_err = linregress(x=df_high['Number'], y=df_high['High'])
    df_high = df_high.loc[df_high['High'] > slope * df_high['Number'] + intercept]
    
print(df_high.tail())
    


# lower points are returned
while len(df_low)>2:
    slope, intercept, r_value, p_value, std_err = linregress(x=df_low['Number'], y=df_low['Low'])
    df_low = df_low.loc[df_low['Low'] < slope * df_low['Number'] + intercept]
    
print(df_low.tail())

#lets take the points in both uptrend and downtrend calc for scipy.stats.lingress method. the method will return a slope,
#interceptiom,p&r values also standard errors of a fnctions

slope, intercept, r_value, p_value, std_err = linregress(x=df_high['Number'], y=df_high['Close'])
df['Uptrend'] = slope * df['Number'] + intercept

slope, intercept, r_value, p_value, std_err = linregress(x=df_low['Number'], y=df_low['Close'])
df['Downtrend'] = slope * df['Number'] + intercept

print(df.tail())


# draw the closing price and related trendlines (uptrend and downtrend)
fig, ax1 = plt.subplots(figsize=(15,10))

color = 'tab:green'
xdate = [x.date() for x in df.index]
ax1.set_xlabel('Date', color=color)
ax1.plot(xdate, df.Close, label="close", color=color)
ax1.tick_params(axis='x', labelcolor=color)
ax1.legend()

ax2 = ax1.twiny() # ax2 and ax1 will have common y axis and different x axis, twiny
ax2.plot(df.Number, df.Uptrend, label="uptrend")
ax2.plot(df.Number, df.Downtrend, label="downtrend")

plt.legend()
plt.grid()
plt.show()