import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)


left_column, right_column = st.columns(2)
with left_column:
# Execute query and fetch results into DataFrame
    query = f"""
    select money,food,coal,oil,uranium,lead,iron,bauxite,gasoline,munitions,steel,aluminum from bankaccounts where nation_id = '{nationid}'
    """
    df = conn.query(query)
    st.markdown("## Bank Account Holdings")
    st.write(df.transpose())
with right_column:
    query2 = f"""
    select soldiers,tanks,aircraft,ships,missile,nukes,spies from tiny_nations where id = '{nationid}'
    """
    df2 = conn.query(query2)
    st.markdown("## Military Info")    
    st.write(df2.transpose())    
    