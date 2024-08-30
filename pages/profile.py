import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")

conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
nationname = st.session_state.nationname
st.markdown(f"# {nationname}'s Porfolio")

st.markdown("## Trade Market Information")

# Fetch the latest trade prices
query0 = """
SELECT Food, Coal, Oil, Uranium, Iron, Bauxite, Lead, Gasoline, Munitions, Steel, Aluminum
FROM tradeprices 
ORDER BY trade_timestamp DESC 
LIMIT 1
"""
df0 = conn.query(query0)
st.write(df0)

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

if st.button("Reload"):
        results = conn.query(query0)  
        st.write("Updated")


# Assuming results is converted to a DataFrame
st.write(results)

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
