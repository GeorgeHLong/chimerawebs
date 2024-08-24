import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)

query = f"""
select capture_date,gdp from nationlog where nation_id = '{nationid}' order by capture_date desc
"""

# Execute query and fetch results into DataFrame
df = conn.query(query)
st.write(df)
