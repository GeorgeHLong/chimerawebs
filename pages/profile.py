import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)


left_column, center,right_column = st.columns(3)
with left_column:
# Execute query and fetch results into DataFrame
    query = f"""
    select money,food,coal,oil,uranium,lead,iron,bauxite,gasoline,munitions,steel,aluminum from bankaccounts where nation_id = '{nationid}'
    """
    df = conn.query(query)
    st.markdown("## Bank Account Holdings")
    st.write(df.transpose())
with center:
    