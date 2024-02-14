import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import sys



if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3']:
    print('Enter a factor num: [1,2,3]')
    exit(0)

factor_num = int(sys.argv[1]) - 1

def calculate_factor_1(df):
    n = 5
    df['Factor'] = ((df['Close'] - df['Close'].shift(n-1)) / df['Close'].shift(n-1)) * 100
    df['Factor'] = df['Factor'].shift(1)
    return df[['Date', 'Factor']].rename(columns={'Factor': ticker})

def calculate_factor_2(df):
    n = 15
    df['Factor'] = ((df['Close'] - df['Close'].shift(n-1)) / df['Close'].shift(n-1)) * 100 / df['Volume'] 
    df['Factor'] = df['Factor'].shift(1)
    return df[['Date', 'Factor']].rename(columns={'Factor': ticker})

def calculate_factor_3(df):
    n= 50
    df['Factor'] = ((df['Open'] - df['Close'].shift(n-1)) / df['Close'].shift(n-1)) * 100 / df['Adj Close'] 
    df['Factor'] = df['Factor'].shift(1)
    return df[['Date', 'Factor']].rename(columns={'Factor': ticker})

mapping = [calculate_factor_1, calculate_factor_2, calculate_factor_3]

with open('../task_1/tickers.txt', 'r') as file:
    tickers = [line.strip() for line in file]

start_date = '2021-01-01'
end_date = '2023-12-31'
n = 5  

data_folder = '../data/'
factor_folder = './'

if not os.path.exists(factor_folder):
    os.makedirs(factor_folder)

factors_df = pd.DataFrame()

for ticker in tickers:
    try:
        stock_data = pd.read_csv(f'{data_folder}{ticker}.csv', parse_dates=True)
        factor_data = mapping[factor_num](stock_data)
        factors_df = pd.concat([factors_df, factor_data.set_index('Date')], axis=1)

        print(f'Successfully calculated factor for {ticker}')

    except Exception as e:
        print(f'Error calculating factor for {ticker}: {e}')

# Save the factors data to a CSV file
factors_df.to_csv(f'{factor_folder}factors_{str(factor_num+1)}.csv')

print('Factor calculation completed.')
