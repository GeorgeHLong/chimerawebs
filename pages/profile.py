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


