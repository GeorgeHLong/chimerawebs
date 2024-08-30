import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Display the banner image
st.image("images/banner.png")

conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
nationname = st.session_state.nationname
st.markdown(f"# {nationname}'s Porfolio")

st.markdown("## Trade Market Information")

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

        
query = f"""
SELECT money, food, coal, oil, uranium, lead, iron, bauxite, gasoline, munitions, steel, aluminum 
FROM bankaccounts 
WHERE nation_id = {nationid}
"""
left_column, right_column = st.columns(2)
with left_column:
        df = conn.query(query)
        st.markdown("## Chimera Holdings")
        st.write(df.transpose())
query00 = f"""
SELECT money, food, coal, oil, uranium, lead, iron, bauxite, gasoline, munitions, steel, aluminum 
FROM bankaccounts 
WHERE nation_id = {nationid}
"""
results = conn.query(query00)




# Assuming results is converted to a DataFrame
st.write(results)

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
    fig_24h = px.line(df_24h, x='trade_timestamp', y=df_24h.columns[1:], title='Prices Over the Last 24 Hours')
    st.plotly_chart(fig_24h)
else:
    st.write("No data available for the last 24 hours.")

# Create a plot for the past 7 days
st.markdown("### Price Trends in the Last 7 Days")
if not df_7d.empty:
    fig_7d = px.line(df_7d, x='trade_timestamp', y=df_7d.columns[1:], title='Prices Over the Last 7 Days')
    st.plotly_chart(fig_7d)
else:
    st.write("No data available for the last 7 days.")

# Display raw data tables for 24 hours and 7 days
st.markdown("### Raw Data: Last 24 Hours")
st.write(df_24h)

st.markdown("### Raw Data: Last 7 Days")
st.write(df_7d)

# Get all resource values
money = results.at[0, 'money']
food = results.at[0, 'food']
coal = results.at[0, 'coal']
oil = results.at[0, 'oil']
uranium = results.at[0, 'uranium']
lead = results.at[0, 'lead']
iron = results.at[0, 'iron']
bauxite = results.at[0, 'bauxite']
gasoline = results.at[0, 'gasoline']
munitions = results.at[0, 'munitions']
steel = results.at[0, 'steel']
aluminum = results.at[0, 'aluminum']

# Display metrics side by side
cols = st.columns(6)

cols[0].metric(label="Money", value=f"${money:,.2f}")
cols[1].metric(label="Food", value=f"{food:,.2f}")
cols[2].metric(label="Coal", value=f"{coal:,.2f}")
cols[3].metric(label="Oil", value=f"{oil:,.2f}")
cols[4].metric(label="Uranium", value=f"{uranium:,.2f}")
cols[5].metric(label="Lead", value=f"{lead:,.2f}")

cols = st.columns(6)

cols[0].metric(label="Iron", value=f"{iron:,.2f}")
cols[1].metric(label="Bauxite", value=f"{bauxite:,.2f}")
cols[2].metric(label="Gasoline", value=f"{gasoline:,.2f}")
cols[3].metric(label="Munitions", value=f"{munitions:,.2f}")
cols[4].metric(label="Steel", value=f"{steel:,.2f}")
cols[5].metric(label="Aluminum", value=f"{aluminum:,.2f}")
