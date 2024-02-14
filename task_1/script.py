import yfinance as yf
import pandas as pd
from datetime import datetime

with open('tickers.txt', 'r') as file:
    tickers = [line.strip() for line in file]

start_date = '2021-01-01'
end_date = '2023-12-31'

data_folder = '../data/'
import os
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

num_data_points = None
for ticker in tickers:
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']]
        
        if stock_data.isnull().values.any():
            stock_data = stock_data.dropna()
        
        stock_data.index = pd.to_datetime(stock_data.index)

        stock_data.to_csv(f'{data_folder}{ticker}.csv')

        if num_data_points is None:
            num_data_points = len(stock_data)
        else:
            assert num_data_points == len(stock_data), f'Data inconsistency for {ticker}'

        print(f'Successfully retrieved and processed data for {ticker}')

    except Exception as e:
        print(f'Error retrieving or processing data for {ticker}: {e}')

print('Data collection and processing completed.')
