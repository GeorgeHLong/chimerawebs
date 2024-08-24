import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
st.markdown("## Trade Market Information")

# Fetch the latest trade prices
query0 = """
SELECT Food, Coal, Oil, Uranium, Iron, Bauxite, Lead, Gasoline, Munitions, Aluminum, Steel 
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
df = conn.query(query)
st.markdown("## Chimera Holdings")
st.write(df.transpose())

# Military Info
query3 = """
SELECT ROUND(AVG(soldiers), 0) AS soldiers, ROUND(AVG(tanks), 0) AS tanks, 
        ROUND(AVG(aircraft), 0) AS aircraft, ROUND(AVG(ships), 0) AS ships, 
        ROUND(AVG(missiles), 0) AS missiles, ROUND(AVG(nukes), 0) AS nukes, 
        ROUND(AVG(spies), 0) AS spies 
FROM tiny_nations 
WHERE score BETWEEN 8000 AND 9000
"""
df3 = conn.query(query3).transpose()

query2 = f"""
SELECT soldiers, tanks, aircraft, ships, missiles, nukes, spies 
FROM tiny_nations 
WHERE id = {nationid}
"""
df2 = conn.query(query2).transpose()

# Combine your data with the average for comparison
merged = pd.concat([df2, df3], axis=1)
merged.columns = ["Your Forces", "Average Forces"]

st.line_chart(merged)


# Plotting side by side comparison
fig = px.bar(merged, barmode='group', title="Your Military Forces vs Average Forces")
st.bar_chart(merged)
