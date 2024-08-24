import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid =  st.session_state.role
query = f"""
select * from tiny_nations tn where tn.id = '{nationid}'
"""

# Execute query and fetch results into DataFrame
df = conn.query(query)
st.write(df)
