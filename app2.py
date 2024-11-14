import pandas as pd

# Load your data and save it as a pickle file
data = pd.read_excel("bitcoin.xlsx", parse_dates=['Date'])
data.to_pickle("data.pkl")


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pickle

# Load Bitcoin price data from pickle file
with open("data.pkl", "rb") as f:
    data = pickle.load(f)
data.set_index('Date', inplace=True)

# Simulate Buy/Sell signals as per backtest conditions
data['Buy_Entry'] = np.where(data['Close'] > data['Close'].rolling(10).mean(), 1, 0)
data['Buy_Exit'] = np.where(data['Close'] < data['Close'].rolling(10).mean(), 1, 0)
data['Sell_Entry'] = np.where(data['Close'] < data['Close'].rolling(10).mean(), 1, 0)
data['Sell_Exit'] = np.where(data['Close'] > data['Close'].rolling(10).mean(), 1, 0)

# Tracking positions and profit for live plotting
position = 0
entry_price = 0
profits = []
cumulative_profits = [0]
daily_cumulative_profits = [0] * len(data)

for i in range(1, len(data)):
    if data['Buy_Entry'].iloc[i] == 1 and position == 0:
        position = 1
        entry_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
    elif data['Buy_Exit'].iloc[i] == 1 and position == 1:
        exit_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
        profit = exit_price - entry_price
        profits.append(profit)
        cumulative_profits.append(cumulative_profits[-1] + profit)
        position = 0
    elif data['Sell_Entry'].iloc[i] == 1 and position == 0:
        position = -1
        entry_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
    elif data['Sell_Exit'].iloc[i] == 1 and position == -1:
        exit_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
        profit = entry_price - exit_price
        profits.append(profit)
        cumulative_profits.append(cumulative_profits[-1] + profit)
        position = 0

    daily_cumulative_profits[i] = cumulative_profits[-1]

data['Cumulative_Profit'] = daily_cumulative_profits

# Streamlit Dashboard
st.title("Bitcoin Trading Backtest Dashboard")

# Plotly interactive plot
fig = go.Figure()

# Plot Bitcoin price
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Bitcoin Price', line=dict(color='blue')))

# Mark Buy/Sell points
fig.add_trace(go.Scatter(x=data[data['Buy_Entry'] == 1].index, y=data[data['Buy_Entry'] == 1]['Close'],
                         mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=10)))
fig.add_trace(go.Scatter(x=data[data['Sell_Entry'] == 1].index, y=data[data['Sell_Entry'] == 1]['Close'],
                         mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=10)))

# Plot cumulative profits
fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Profit'], mode='lines', name='Cumulative Profit', line=dict(color='orange', dash='dash')))

# Customize layout
fig.update_layout(title='Bitcoin Price and Backtest Signals', xaxis_title='Date', yaxis_title='Price / Cumulative Profit', template='plotly_dark')

# Display plot
st.plotly_chart(fig)
