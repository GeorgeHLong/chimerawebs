import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Display the banner image
st.image("images/banner.png")

conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
nationname = st.session_state.nationname
st.markdown(f"# {nationname}'s Porfolio")



        

st.markdown("## Chimera Holdings")
query00 = f"""
SELECT money, food, coal, oil, uranium, lead, iron, bauxite, gasoline, munitions, steel, aluminum 
FROM bankaccounts 
WHERE nation_id = {nationid}
"""
results = conn.query(query00)

# Get all resource values
money = results.at[0, 'money']
food = results.at[0, 'food']
coal = results.at[0, 'coal']
oil = results.at[0, 'oil']
uranium = results.at[0, 'uranium']
lead = results.at[0, 'lead']
iron = results.at[0, 'iron']
bauxite = results.at[0, 'bauxite']
gasoline = results.at[0, 'gasoline']
munitions = results.at[0, 'munitions']
steel = results.at[0, 'steel']
aluminum = results.at[0, 'aluminum']

# Display metrics side by side
cols = st.columns(2)

cols[0].metric(label="Money", value=f"${money:,.2f}")
cols[1].metric(label="Food", value=f"{food:,.2f}")
cols[0].metric(label="Coal", value=f"{coal:,.2f}")
cols[1].metric(label="Oil", value=f"{oil:,.2f}")
cols[0].metric(label="Uranium", value=f"{uranium:,.2f}")
cols[1].metric(label="Lead", value=f"{lead:,.2f}")

cols = st.columns(2)

cols[0].metric(label="Iron", value=f"{iron:,.2f}")
cols[1].metric(label="Bauxite", value=f"{bauxite:,.2f}")
cols[0].metric(label="Gasoline", value=f"{gasoline:,.2f}")
cols[1].metric(label="Munitions", value=f"{munitions:,.2f}")
cols[0].metric(label="Steel", value=f"{steel:,.2f}")
cols[1].metric(label="Aluminum", value=f"{aluminum:,.2f}")

st.markdown("## Your MMR Average")
query02 = f"""
SELECT avg(barracks) as avg_barracks, avg(factory) as avg_factory, avg(hangar) as avg_hangar, avg(drydock) as avg_drydock
FROM cities 
WHERE nation_id = {nationid}
"""
results = conn.query(query02)

# Extract the average values for the city infrastructure
avg_barracks = results.at[0, 'avg_barracks']
avg_factory = results.at[0, 'avg_factory']
avg_hangar = results.at[0, 'avg_hangar']
avg_drydock = results.at[0, 'avg_drydock']

# Display metrics side by side
cols = st.columns(2)

cols[0].metric(label="Average Barracks", value=f"{avg_barracks:,.2f}")
cols[1].metric(label="Average Factory", value=f"{avg_factory:,.2f}")
cols[0].metric(label="Average Hangar", value=f"{avg_hangar:,.2f}")
cols[1].metric(label="Average Drydock", value=f"{avg_drydock:,.2f}")