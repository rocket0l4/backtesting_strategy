# import pandas as pd
#
# # Load your data and save it as a pickle file
# data = pd.read_excel("bitcoin.xlsx", parse_dates=['Date'])
# data.to_pickle("data.pkl")
#
#
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import streamlit as st
# import pickle
#
# # Load Bitcoin price data from pickle file
# with open("data.pkl", "rb") as f:
#     data = pickle.load(f)
# data.set_index('Date', inplace=True)
#
# # Simulate Buy/Sell signals as per backtest conditions
# data['Buy_Entry'] = np.where(data['Close'] > data['Close'].rolling(10).mean(), 1, 0)
# data['Buy_Exit'] = np.where(data['Close'] < data['Close'].rolling(10).mean(), 1, 0)
# data['Sell_Entry'] = np.where(data['Close'] < data['Close'].rolling(10).mean(), 1, 0)
# data['Sell_Exit'] = np.where(data['Close'] > data['Close'].rolling(10).mean(), 1, 0)
#
# # Tracking positions and profit for live plotting
# position = 0
# entry_price = 0
# profits = []
# cumulative_profits = [0]
# daily_cumulative_profits = [0] * len(data)
#
# for i in range(1, len(data)):
#     if data['Buy_Entry'].iloc[i] == 1 and position == 0:
#         position = 1
#         entry_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
#     elif data['Buy_Exit'].iloc[i] == 1 and position == 1:
#         exit_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
#         profit = exit_price - entry_price
#         profits.append(profit)
#         cumulative_profits.append(cumulative_profits[-1] + profit)
#         position = 0
#     elif data['Sell_Entry'].iloc[i] == 1 and position == 0:
#         position = -1
#         entry_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
#     elif data['Sell_Exit'].iloc[i] == 1 and position == -1:
#         exit_price = data['Open'].iloc[i + 1] if i + 1 < len(data) else data['Open'].iloc[i]
#         profit = entry_price - exit_price
#         profits.append(profit)
#         cumulative_profits.append(cumulative_profits[-1] + profit)
#         position = 0
#
#     daily_cumulative_profits[i] = cumulative_profits[-1]
#
# data['Cumulative_Profit'] = daily_cumulative_profits
#
# # Streamlit Dashboard
# st.title("Bitcoin Trading Backtest Dashboard")
#
# # Plotly interactive plot
# fig = go.Figure()
#
# # Plot Bitcoin price
# fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Bitcoin Price', line=dict(color='blue')))
#
# # Mark Buy/Sell points
# fig.add_trace(go.Scatter(x=data[data['Buy_Entry'] == 1].index, y=data[data['Buy_Entry'] == 1]['Close'],
#                          mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=10)))
# fig.add_trace(go.Scatter(x=data[data['Sell_Entry'] == 1].index, y=data[data['Sell_Entry'] == 1]['Close'],
#                          mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=10)))
#
# # Plot cumulative profits
# fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Profit'], mode='lines', name='Cumulative Profit', line=dict(color='orange', dash='dash')))
#
# # Customize layout
# fig.update_layout(title='Bitcoin Price and Backtest Signals', xaxis_title='Date', yaxis_title='Price / Cumulative Profit', template='plotly_dark')
#
# # Display plot
# st.plotly_chart(fig)
#
#
# # Streamlit Dashboard
# st.title("Bitcoin Trading Backtest Dashboard 2")
#
# # Plotly candlestick chart
# fig = go.Figure()
#
# # Add candlestick chart
# fig.add_trace(
#     go.Candlestick(
#         x=data.index,
#         open=data['Open'],
#         high=data['High'],
#         low=data['Low'],
#         close=data['Close'],
#         name='Candlestick',
#     )
# )
#
# # Mark Buy/Sell points
# fig.add_trace(go.Scatter(
#     x=data[data['Buy_Entry'] == 1].index,
#     y=data[data['Buy_Entry'] == 1]['Close'],
#     mode='markers',
#     name='Buy Signal',
#     marker=dict(color='green', symbol='triangle-up', size=10)
# ))
# fig.add_trace(go.Scatter(
#     x=data[data['Sell_Entry'] == 1].index,
#     y=data[data['Sell_Entry'] == 1]['Close'],
#     mode='markers',
#     name='Sell Signal',
#     marker=dict(color='red', symbol='triangle-down', size=10)
# ))
#
# # Plot cumulative profits as a separate line
# fig.add_trace(go.Scatter(
#     x=data.index,
#     y=data['Cumulative_Profit'],
#     mode='lines',
#     name='Cumulative Profit',
#     line=dict(color='orange', dash='dash')
# ))
#
# # Customize layout
# fig.update_layout(
#     title='Bitcoin Candlestick Chart with Backtest Signals',
#     xaxis_title='Date',
#     yaxis_title='Price',
#     template='plotly_dark',
#     xaxis_rangeslider_visible=False  # Optional: Hide the default range slider
# )
#
# # Display the plot in Streamlit
# st.plotly_chart(fig)
#



import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pickle

# Load Bitcoin price data from pickle file
with open("data.pkl", "rb") as f:
    data = pickle.load(f)
data.set_index('Date', inplace=True)

# Filter data for a specific price range
min_price = 20000  # Set your minimum price here
max_price = 40000  # Set your maximum price here
filtered_data = data[(data['Close'] >= min_price) & (data['Close'] <= max_price)]

# Ensure there's data to plot
if filtered_data.empty:
    st.error(f"No data available for the price range {min_price}-{max_price}. Please adjust the range.")
else:
    # Simulate Buy/Sell signals as per backtest conditions
    filtered_data['Buy_Entry'] = np.where(filtered_data['Close'] > filtered_data['Close'].rolling(10).mean(), 1, 0)
    filtered_data['Sell_Entry'] = np.where(filtered_data['Close'] < filtered_data['Close'].rolling(10).mean(), 1, 0)

    # Streamlit Dashboard
    st.title("Bitcoin Trading Dashboard (Filtered by Price Range)")

    # Plotly interactive plot
    fig = go.Figure()

    # Plot Bitcoin price
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['Close'],
        mode='lines', name='Bitcoin Price', line=dict(color='blue')
    ))

    # Mark Buy/Sell points
    fig.add_trace(go.Scatter(
        x=filtered_data[filtered_data['Buy_Entry'] == 1].index,
        y=filtered_data[filtered_data['Buy_Entry'] == 1]['Close'],
        mode='markers', name='Buy Signal',
        marker=dict(color='green', symbol='triangle-up', size=10)
    ))
    fig.add_trace(go.Scatter(
        x=filtered_data[filtered_data['Sell_Entry'] == 1].index,
        y=filtered_data[filtered_data['Sell_Entry'] == 1]['Close'],
        mode='markers', name='Sell Signal',
        marker=dict(color='red', symbol='triangle-down', size=10)
    ))

    # Customize layout
    fig.update_layout(
        title=f"Bitcoin Price (Filtered: {min_price}-{max_price})",
        xaxis_title='Date', yaxis_title='Price',
        template='plotly_dark'
    )

    # Display plot
    st.plotly_chart(fig)

# Streamlit Dashboard
    st.title(f"Bitcoin Candlestick Chart (Filtered: {min_price}-{max_price})")

    # Plotly candlestick chart
    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=filtered_data.index,
        open=filtered_data['Open'],
        high=filtered_data['High'],
        low=filtered_data['Low'],
        close=filtered_data['Close'],
        name='Candlestick',
    ))

    # Mark Buy/Sell points
    fig.add_trace(go.Scatter(
        x=filtered_data[filtered_data['Buy_Entry'] == 1].index,
        y=filtered_data[filtered_data['Buy_Entry'] == 1]['Close'],
        mode='markers',
        name='Buy Signal',
        marker=dict(color='green', symbol='triangle-up', size=10)
    ))
    fig.add_trace(go.Scatter(
        x=filtered_data[filtered_data['Sell_Entry'] == 1].index,
        y=filtered_data[filtered_data['Sell_Entry'] == 1]['Close'],
        mode='markers',
        name='Sell Signal',
        marker=dict(color='red', symbol='triangle-down', size=10)
    ))

    # Customize layout
    fig.update_layout(
        title=f"Bitcoin Candlestick Chart (Filtered: {min_price}-{max_price})",
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False  # Optional: Hide the range slider
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)