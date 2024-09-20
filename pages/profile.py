import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

conn = st.connection("postgresql", type="sql")
nationid = int(st.session_state.role)
nationname = st.session_state.nationname
alliancename = st.session_state.alliancename
role = st.session_state.allianceposition
username = st.session_state.username
role = role.title()

profile_image_url = "https://cdn-icons-png.flaticon.com/512/6596/6596121.png"
st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: flex-end; padding: 10px; border: 1px solid #ddd; border-radius: 10px; background-color: #0000;">
        <div style="margin-right: 10px;">
            <img src="{profile_image_url}" alt="Profile Image" style="width: 50px; height: 50px; border-radius: 50%;">
        </div>
        <div style="text-align: left;">
            <p style="margin: 0; font-weight: bold;">{username}</p>
            <p style="margin: 0;">Alliance: {alliancename}</p>
            <p style="margin: 0;">Role: {role}</p><br/>
        </div>
    </div>
""", unsafe_allow_html=True)# Display the banner image
st.image("images/banner.png")


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


st.empty()
st.markdown("<br><br>", unsafe_allow_html=True)  # Adds two line breaks
st.markdown("## Military Composition")
query02 = f"""
SELECT avg(barracks) as avg_barracks, avg(factory) as avg_factory, avg(hangar) as avg_hangar, avg(drydock) as avg_drydock
FROM cities 
WHERE nation_id = {nationid}
"""
results = conn.query(query02)

# Extract the average values for the city infrastructure
avg_barracks1 = results.at[0, 'avg_barracks']
avg_factory1 = results.at[0, 'avg_factory']
avg_hangar1 = results.at[0, 'avg_hangar']
avg_drydock1 = results.at[0, 'avg_drydock']

query03 = f"""
SELECT tn.alliance_id, 
       AVG(cities.barracks) AS avg_barracks, 
       AVG(cities.factory) AS avg_factory, 
       AVG(cities.hangar) AS avg_hangar, 
       AVG(cities.drydock) AS avg_drydock
FROM cities
JOIN tiny_nations tn ON tn.id = cities.nation_id
JOIN alliances a ON a.alliance_id = tn.alliance_id
WHERE tn.alliance_id = (SELECT tn2.alliance_id FROM tiny_nations tn2 WHERE tn2.id = {nationid} and tn.tax_id != 0)
GROUP BY tn.alliance_id; 
"""
results = conn.query(query03)

# Extract the average values for the city infrastructure
avg_barracks = results.at[0, 'avg_barracks']
avg_factory = results.at[0, 'avg_factory']
avg_hangar = results.at[0, 'avg_hangar']
avg_drydock = results.at[0, 'avg_drydock']



# Your average city infrastructure
your_avg = [avg_barracks1, avg_factory1, avg_hangar1, avg_drydock1]

# Alliance average city infrastructure
alliance_avg = [results.at[0, 'avg_barracks'], results.at[0, 'avg_factory'], results.at[0, 'avg_hangar'], results.at[0, 'avg_drydock']]

# Labels for the infrastructure
labels = ['Barracks', 'Factory', 'Hangar', 'Drydock']

# Create the figure using Plotly
fig = go.Figure()

# Add bars for your averages
fig.add_trace(go.Bar(
    x=labels,
    y=your_avg,
    name='Your Avg',
    marker_color='blue'
))

# Add bars for the alliance averages
fig.add_trace(go.Bar(
    x=labels,
    y=alliance_avg,
    name='Alliance Avg',
    marker_color='green'
))

# Set the layout for the chart
fig.update_layout(
    title='MMR Comparison',
    xaxis_title='Military Building',
    yaxis_title='Average Value',
    barmode='group',  # To place bars side by side
    plot_bgcolor='rgba(0,0,0,0)',
)

# Display the chart in Streamlit
st.plotly_chart(fig)

# Display metrics side by side
cols = st.columns(2)
# Display metrics side by side
cols[1].markdown("## Alliance Avg.")

cols[1].metric(label="Average Barracks", value=f"{avg_barracks:,.2f}")
cols[1].metric(label="Average Factory", value=f"{avg_factory:,.2f}")
cols[1].metric(label="Average Hangar", value=f"{avg_hangar:,.2f}")
cols[1].metric(label="Average Drydock", value=f"{avg_drydock:,.2f}")
cols[0].markdown("## Your Avg.")
cols[0].metric(label="Average Barracks", value=f"{avg_barracks1:,.2f}")
cols[0].metric(label="Average Factory", value=f"{avg_factory1:,.2f}")
cols[0].metric(label="Average Hangar", value=f"{avg_hangar1:,.2f}")
cols[0].metric(label="Average Drydock", value=f"{avg_drydock1:,.2f}")