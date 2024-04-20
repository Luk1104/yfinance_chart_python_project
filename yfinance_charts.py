import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from tradingview_ta import TA_Handler , Interval , get_multiple_analysis

cr_assets = []
cr_assets_ta = []
#zczytywanie inputu usera
while True:
    answer = input("Podaj coin (np. BTC): ")
    if answer=='':
        break
    answer=answer.upper()
    cr_assets.append(answer+'-USD')
    cr_assets_ta.append('BINANCE:'+answer+'USD')

#TA stuff

analysis = get_multiple_analysis(screener="crypto", interval=Interval.INTERVAL_1_DAY, symbols=cr_assets_ta)
symbols=cr_assets_ta

for symbol in symbols:
    print(symbol, "price", analysis[symbol].indicators["close"], "USD")

print()
print("EMA30:")

for symbol in symbols:
    print(symbol, analysis[symbol].indicators["EMA30"])

print()
print('RSI:')

for symbol in symbols:
    print(symbol, analysis[symbol].indicators["RSI"])


#dla 1 coina
if len(cr_assets)==1:
    asset = cr_assets[0]
    crypto_data = yf.Ticker(asset).history(period='1y')

    crypto_data['EMA30'] = crypto_data['Close'].ewm(span=30, adjust=False).mean()

    #liczenie RSI

    crypto_data['Price Change'] = crypto_data['Close'].diff()

    crypto_data['PosRSI'] = crypto_data['Price Change'].apply(lambda x: x if x > 0 else 0)
    crypto_data['NegRSI'] = crypto_data['Price Change'].apply(lambda x: -x if x < 0 else 0)
    
    crypto_data['Avg+'] = crypto_data['PosRSI'].rolling(14).mean()
    crypto_data['Avg-'] = crypto_data['NegRSI'].rolling(14).mean()

    crypto_data['RS'] = crypto_data['Avg+']/crypto_data['Avg-']
    crypto_data['RSI'] = 100 - (100/(1 + crypto_data['RS']))

    #wykres

    fig, (chart1, chart2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    #plt.title(f'{asset} Price')
    fig.suptitle(f'{asset} Price and RSI')
    #plt.ylabel('Price ($)')
    plt.xlabel('Date')
    chart1.plot(crypto_data.index, crypto_data['Close'], label='Price')
    chart1.plot(crypto_data.index, crypto_data['EMA30'], label='EMA30', color='red')
    chart2.plot(crypto_data.index, crypto_data['RSI'], label='RSI', color='purple')
    chart1.grid(True)
    chart2.grid(True)
    chart1.legend(cr_assets)
    plt.show()

else:
    #wykres
    df=pd.DataFrame()

    for asset in cr_assets:
        df[asset] = yf.Ticker(asset).history(interval='1d',period='1y').Close

    plt.figure()
    plt.plot(df)
    plt.title(f'Comparison of {cr_assets}')
    plt.ylabel('Price ($)')
    plt.xlabel('Date')
    plt.grid(True)
    plt.legend(cr_assets)
    plt.show()
