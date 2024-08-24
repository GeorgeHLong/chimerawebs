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

left_column, center = st.columns(2)

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
with center:
    query3 = f"""
    select round(avg(soldiers), 0) as "avg_soldiers", round(avg(tanks), 0) as "avg_tanks", 
           round(avg(aircraft), 0) as "avg_aircraft", round(avg(ships), 0) as "avg_ships", 
           round(avg(missiles), 0) as "avg_missiles", round(avg(nukes), 0) as "avg_nukes", 
           round(avg(spies), 0) as "avg_spies" 
    from tiny_nations tn 
    where score between 8000 and 9000
    """
    df3 = conn.query(query3)
    st.markdown("## Average Military Info")
    st.write(df3.transpose())

    query2 = f"""
    select soldiers, tanks, aircraft, ships, missiles, nukes, spies 
    from tiny_nations 
    where id = '{nationid}'
    """
    df2 = conn.query(query2)
    st.markdown("## Your Military Info")
    st.write(df2.transpose())

# Combine DataFrames and Create Bar Chart
# Rename columns to distinguish between "Your" and "Average"
df2.columns = ['Your Soldiers', 'Your Tanks', 'Your Aircraft', 'Your Ships', 'Your Missiles', 'Your Nukes', 'Your Spies']
df3.columns = ['Avg Soldiers', 'Avg Tanks', 'Avg Aircraft', 'Avg Ships', 'Avg Missiles', 'Avg Nukes', 'Avg Spies']

# Combine the DataFrames side by side
combined_df = pd.concat([df2.transpose(), df3.transpose()], axis=1)
combined_df.columns = ['Your Value', 'Average Value']
combined_df['Category'] = combined_df.index

# Reset index for plotting
combined_df = combined_df.reset_index(drop=True)

# Melt the DataFrame for Plotly
combined_df = combined_df.melt(id_vars='Category', value_vars=['Your Value', 'Average Value'], 
                                var_name='Type', value_name='Count')

# Create the bar chart
fig = px.bar(combined_df, x='Category', y='Count', color='Type', barmode='group', 
                labels={'Count': 'Military Units', 'Category': 'Military Type'})

st.plotly_chart(fig)
