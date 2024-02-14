import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class BacktestStrategy:
    def __init__(self, factor_file, data_folder):
        self.factors = pd.read_csv(factor_file, index_col=0)
        self.data = {ticker: pd.read_csv(f'{data_folder}/{ticker}.csv', index_col='Date') 
                     for ticker in self.factors.columns}

    def calculate_returns(self):
        top_5_returns = []
        even_returns = []

        for date, row in self.factors.iterrows():
            sorted_tickers = row.sort_values(ascending=False)
            top_5_tickers = sorted_tickers.nlargest(5).index

            

            # Calculate returns for top 5 and even positions
            top_5_returns.append(self._calculate_daily_return(top_5_tickers, date))
            even_returns.append(self._calculate_daily_return(self.factors.columns, date))

        return top_5_returns, even_returns

    def _calculate_daily_return(self, tickers, date):
        # Calculate daily return for given tickers
        return sum(self._ticker_return(ticker, date) for ticker in tickers) / len(tickers)

    def _ticker_return(self, ticker, date):
        # Calculate return for a single ticker
        try:
            # daily_data = self.data[ticker].loc[date]
            # return daily_data['Close'] / daily_data['Open'] - 1
            # Use iloc to get the index of the current date
            current_index = self.data[ticker].index.get_loc(date)
            
            # Access the next day's data using iloc and shift
            next_day_data = self.data[ticker].iloc[current_index + 1]

            # Calculate return using the next day's Open and Close prices
            return next_day_data['Close'] / next_day_data['Open'] - 1
        except Exception:
            return 0  # Return zero if data is missing

    @staticmethod
    def plot_cumulative_returns(returns, label):
        cumulative_returns = np.cumprod([1 + r for r in returns])
        plt.plot(cumulative_returns, label=label)

def main(factor_file, data_folder):
    strategy = BacktestStrategy(factor_file, data_folder)
    top_5_returns, even_returns = strategy.calculate_returns()

    # Plotting the results
    strategy.plot_cumulative_returns(top_5_returns, 'Top 5')
    strategy.plot_cumulative_returns(even_returns, 'Even')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run backtesting strategy.')
    parser.add_argument('factor_file', type=str, help='Path to the factor CSV file')
    parser.add_argument('data_folder', type=str, help='Path to the folder containing ticker data')
    
    args = parser.parse_args()
    main(args.factor_file, args.data_folder)