import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Display the banner image
st.image("images/banner.png")

conn = st.connection("postgresql", type="sql")


st.markdown("## Trade Market Information")

st.markdown("### Current Sell Market Price Information")

def get_trade_market():
    # Fetch the latest trade prices
    query0 = """
    SELECT Food, Coal, Oil, Uranium, Iron, Bauxite, Lead, Gasoline, Munitions, Steel, Aluminum
    FROM tradeprices 
    ORDER BY trade_timestamp DESC 
    LIMIT 1
    """
    df0 = conn.query(query0)     
    return df0  
       
# Create a placeholder for the table
placeholder = st.empty()

# Display the market information by default
df0 = get_trade_market()
table = placeholder.write(df0)

# Add an update button to refresh the data
if st.button("Update Market Information"):
    df0 = get_trade_market()  # Fetch the updated data
    placeholder.write(df0)  # Update the displayed data in the same placeholder
    
    
st.markdown("### Trade Market Candlestick Graph")

# Define the list of resources and time units
resources = ['Food', 'Coal', 'Oil', 'Uranium', 'Iron', 'Bauxite', 'Lead', 'Gasoline', 'Munitions', 'Steel', 'Aluminum']
time_units = ['hour', 'day']

# Create a form for user input
with st.form(key='trade_market_form'):
    # Dropdown menu to select a resource
    selected_resource = st.selectbox("Select a resource:", resources)

    # Dropdown menu to select the time unit
    selected_time_unit = st.selectbox("Select time unit:", time_units)

    # Slider to select the duration of time (e.g., number of hours or days)
    if selected_time_unit == 'hour':
        duration = st.slider("Select duration (hours):", min_value=1, max_value=72, value=24)
    else:
        duration = st.slider("Select duration (days):", min_value=1, max_value=30, value=7)

    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# Function to fetch OHLC data based on the selected parameters
def get_ohlc_data(time_unit, duration, resource):
    timeframe = datetime.now() - timedelta(**{time_unit + 's': duration})
    
    query = f"""
    WITH base_data AS (
        SELECT 
            DATE_TRUNC('{time_unit}', trade_timestamp) as period,
            {resource} as price,
            trade_timestamp
        FROM tradeprices
        WHERE trade_timestamp >= '{timeframe}'
    ),
    ohlc_open_close AS (
        SELECT 
            period,
            FIRST_VALUE(price) OVER (PARTITION BY period ORDER BY trade_timestamp ASC) as open,
            LAST_VALUE(price) OVER (PARTITION BY period ORDER BY trade_timestamp DESC) as close
        FROM base_data
    ),
    ohlc_data AS (
        SELECT 
            period,
            MIN(price) as low, 
            MAX(price) as high
        FROM base_data
        GROUP BY period
    )
    SELECT 
        ohlc_data.period,
        ohlc_data.low,
        ohlc_data.high,
        ohlc_open_close.open,
        ohlc_open_close.close
    FROM ohlc_data
    JOIN ohlc_open_close ON ohlc_data.period = ohlc_open_close.period
    ORDER BY ohlc_data.period ASC
    """
    df = conn.query(query)
    return df

# If the form is submitted, fetch and display the data
if submit_button:
    df = get_ohlc_data(selected_time_unit, duration, selected_resource)

    # Create a candlestick chart
    st.markdown(f"### Last {duration} {selected_time_unit}(s) - {selected_resource}")
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(x=df['period'],
                                             open=df['open'],
                                             high=df['high'],
                                             low=df['low'],
                                             close=df['close'])])
        fig.update_layout(title=f'{selected_resource} Prices Over the Last {duration} {selected_time_unit}(s)', 
                          xaxis_title='Time', yaxis_title='Price')
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for the last {duration} {selected_time_unit}(s).")
 
    
    
def get_trade_data(timeframe):
    query = f"""
    SELECT trade_timestamp, Food, Coal, Oil, Uranium, Iron, Bauxite, Lead, Gasoline, Munitions, Steel, Aluminum
    FROM tradeprices 
    WHERE trade_timestamp >= '{timeframe}'
    ORDER BY trade_timestamp DESC
    """
    df = conn.query(query)     
    return df

# Get the current time and calculate timeframes
now = datetime.now()
time_24h_ago = now - timedelta(hours=24)
time_7d_ago = now - timedelta(days=7)

# Fetch data for the past 24 hours and past 7 days
df_24h = get_trade_data(time_24h_ago)
df_7d = get_trade_data(time_7d_ago)

# Create a plot for the past 24 hours
st.markdown("### Price Trends in the Last 24 Hours")
if not df_24h.empty:
    fig_24h = px.line(df_24h, x='trade_timestamp', y=df_24h.columns[1:])
    st.plotly_chart(fig_24h)
else:
    st.write("No data available for the last 24 hours.")

# Create a plot for the past 7 days
st.markdown("### Price Trends in the Last 7 Days")
if not df_7d.empty:
    fig_7d = px.line(df_7d, x='trade_timestamp', y=df_7d.columns[1:])
    st.plotly_chart(fig_7d)
else:
    st.write("No data available for the last 7 days.")