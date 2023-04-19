import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Sample list of stock tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NFLX", "NVDA", "PYPL", "ADBE"]

# Function to fetch data based on the time frame
def fetch_data(ticker, time_frame, interval):
    data = yf.download(ticker, period=time_frame, interval=interval)
    return data

# Function to create Heikin Ashi candlesticks
def heikin_ashi(data):
    ha_data = data.copy()
    ha_data['HA_Close'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_data['HA_Open'] = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
    ha_data['HA_High'] = data[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    ha_data['HA_Low'] = data[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
    return ha_data

# User inputs for stock selection, time frame, chart type, and indicators
st.sidebar.title("Settings")
selected_ticker = st.sidebar.selectbox("Stock Ticker", tickers, index=0)
selected_time_frame = st.sidebar.selectbox("Time Frame", ["1d", "5d", "1mo", "6mo"], index=0)
selected_interval = st.sidebar.selectbox("Interval", ["1m", "2m", "5m", "10m", "15m"], index=0)
short_ema = st.sidebar.slider("Short EMA Period", min_value=5, max_value=50, value=12, step=1)
long_ema = st.sidebar.slider("Long EMA Period", min_value=20, max_value=200, value=26, step=1)
chart_type = st.sidebar.selectbox("Chart Type", ["Candlestick", "Line"], index=0)

# Fetch the live data and calculate moving averages
data = fetch_data(selected_ticker, selected_time_frame, selected_interval)
data['ema_short'] = data['Close'].ewm(span=short_ema).mean()
data['ema_long'] = data['Close'].ewm(span=long_ema).mean()

if chart_type == "Heikin Ashi":
    data = heikin_ashi(data)

# Create the chart based on the user's chart type selection
fig = go.Figure()

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='Candlestick'))
elif chart_type == "Line":
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))

fig.add_trace(go.Scatter(x=data.index, y=data['ema_short'], mode='lines', name=f'Short EMA ({short_ema})'))
fig.add_trace(go.Scatter(x=data.index, y=data['ema_long'], mode='lines', name=f'Long EMA ({long_ema})'))

fig.update_layout(title=f'{selected_ticker} Live Chart with EMA Crossovers', xaxis_title='Time', yaxis_title='Price')
st.plotly_chart(fig)

# Calculate important metrics
data['returns'] = data['Close'].pct_change()
data['strategy_returns'] = data['returns'] * (data['ema_short'] > data['ema_long'])

cumulative_returns = (1 + data['strategy_returns']).cumprod() - 1
sharpe_ratio = data['strategy_returns'].mean() / data['strategy_returns'].std() * (252 ** 0.5)
max_drawdown = (data['strategy_returns'].cummax() - data['strategy_returns']).max()

# Display metrics in Streamlit app
st.header("Performance Metrics")
st.write(f"Cumulative Returns: {cumulative_returns.iloc[-1]:.2%}")
st.write(f"Sharpe Ratio: {sharpe_ratio:.2f}")
st.write(f"Max Drawdown: {max_drawdown:.2%}")
