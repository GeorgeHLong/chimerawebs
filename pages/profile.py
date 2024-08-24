import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)

query = f"""
select money,food,coal,oil,uranium,lead,iron,bauxite,gasoline,munitions,steel,aluminum from bankaccounts where nation_id = '{nationid}'
"""

# Execute query and fetch results into DataFrame
df = conn.query(query)
st.write(df)
