import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
st.markdown("## Trade Market Information")

query0 = f"""
select Food,Coal,Oil,Uranium,iron,Bauxite,Lead,Gasoline,Munitions,Aluminum,Steel from tradeprices t order by trade_timestamp desc limit 1
"""
df0 = conn.query(query0)
st.write(df0)

left_column, center,right_column = st.columns(3)
with left_column:
# Execute query and fetch results into DataFrame
    query = f"""
    select money,food,coal,oil,uranium,lead,iron,bauxite,gasoline,munitions,steel,aluminum from bankaccounts where nation_id = '{nationid}'
    """
    df = conn.query(query)
    st.markdown("## Chimera Holdings")
    st.write(df.transpose())
with center:
    query3 = f"""
    select round(avg(soldiers),0) as "soldiers", round(avg(tanks),0) as "tanks", round(avg(aircraft),0) as "aircraft", round(avg(ships),0) as "ships", round(avg(missiles),0) as "missiles", round(avg(nukes),0) as "nukes", round(avg(spies),0) as "spies" from tiny_nations tn where score between 8000 and 9000
    """
    df3 = conn.query(query3)
    st.markdown("## Military Info")
    st.write(df3.transpose())    

    query2 = f"""
    select soldiers,tanks,aircraft,ships,missiles,nukes,spies from tiny_nations where id = '{nationid}'
    """
    df2 = conn.query(query2)
    st.markdown("## Military Info")    
    st.write(df2.transpose())
with right_column:
    combined_df = pd.concat([df2, df3], axis=1)
    fig = px.bar(combined_df, x='Category', y=['Value1', 'Value2'], barmode='group')
    st.bar_chart(combined_df,x="Military Info", y="Amount", stack=False)

    