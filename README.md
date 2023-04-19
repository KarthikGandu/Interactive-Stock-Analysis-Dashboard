## Interactive Stock Analysis Dashboard with EMA Crossovers

![icon_logo](https://kajabi-storefronts-production.global.ssl.fastly.net/kajabi-storefronts-production/blogs/2898/images/Zjs3KuNSaS1SfhieVcGX_S_R8.gif)

# Stock Analysis Dashboard with Streamlit

This Python script creates a simple stock analysis dashboard using the Streamlit library. The dashboard allows users to select a stock ticker, time frame, chart type, and moving average settings. It displays a live chart of the stock's price along with short and long exponential moving averages (EMAs). The script also calculates performance metrics such as cumulative returns, Sharpe ratio, and maximum drawdown.

## Requirements

- Python 3.6 or higher
- Streamlit
- yfinance
- pandas
- plotly
- numpy

To install these packages, run:



## How to Run

1. Save the script as `stock_dashboard.py`.
2. In the terminal, navigate to the folder containing the script.
3. Run the command `streamlit run stock_dashboard.py`.
4. A browser window will open, displaying the dashboard.

## Features

- **Settings (sidebar)**: Customize the stock ticker, time frame, chart type, and short/long EMA settings.
- **Live Chart**: Displays a live chart of the stock's price with short and long EMAs.
- **Performance Metrics**: Calculates and displays cumulative returns, Sharpe ratio, and maximum drawdown.

## Code Explanation

1. Import required libraries.
2. Define a sample list of stock tickers.
3. Create a function `fetch_data` that downloads stock data using yfinance based on the user's time frame and interval settings.
4. Create a function `heikin_ashi` that converts regular candlestick data to Heikin Ashi candlesticks.
5. Use Streamlit's sidebar to create user input options for stock ticker, time frame, chart type, and EMA settings.
6. Fetch live data using the `fetch_data` function and calculate short and long EMAs.
7. Generate a live chart using Plotly based on the user's selected chart type.
8. Calculate performance metrics such as cumulative returns, Sharpe ratio, and maximum drawdown.
9. Display the performance metrics in the Streamlit app.

