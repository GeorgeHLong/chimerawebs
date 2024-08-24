import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
st.markdown("## Trade Market Information")

# Fetch the latest trade prices
query0 = f"""
select Food, Coal, Oil, Uranium, iron, Bauxite, Lead, Gasoline, Munitions, Aluminum, Steel 
from tradeprices t 
order by trade_timestamp desc limit 1
"""
df0 = conn.query(query0)
st.write(df0)

left_column, right_column = st.columns(2)

# Chimera Holdings
with left_column:
    query = f"""
    select money, food, coal, oil, uranium, lead, iron, bauxite, gasoline, munitions, steel, aluminum 
    from bankaccounts 
    where nation_id = '{nationid}'
    """
    df = conn.query(query)
    st.markdown("## Chimera Holdings")
    st.write(df.transpose())

# Military Info
with right_column:
    query3 = f"""
    select round(avg(soldiers), 0) as "soldiers", round(avg(tanks), 0) as "tanks", 
           round(avg(aircraft), 0) as "aircraft", round(avg(ships), 0) as "ships", 
           round(avg(missiles), 0) as "missiles", round(avg(nukes), 0) as "nukes", 
           round(avg(spies), 0) as "spies" 
    from tiny_nations tn 
    where score between 8000 and 9000
    """
    df3 = conn.query(query3)


    query2 = f"""
    select soldiers, tanks, aircraft, ships, missiles, nukes, spies 
    from tiny_nations 
    where id = '{nationid}'
    """
    df2 = conn.query(query2)
    df2 = df2.transpose()
    df3 = df3.transpose()
    merged = pd.concat([df2,df3],axis=1)
    st.markdown("## Your Military Info")
    st.write(merged)



