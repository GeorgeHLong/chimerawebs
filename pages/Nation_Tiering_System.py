import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")

# Connect to the database
conn = st.connection("postgresql", type="sql")

# Set the title of the app
st.markdown("# Avg. City Revenue by Alliance")
st.write("Find how alliance's city revenue changed over time and compare between alliances")
def ma_inf(allianceids, days):
    # Define SQL query
    query = f"""
    SELECT capture_date, alliance_id, (totalgdp / totalcities / 365.25) AS avg_daily_income
    FROM alliance_city_distribution
    WHERE alliance_id IN ({allianceids}) AND capture_date BETWEEN CURRENT_DATE - INTERVAL '{days} days' AND CURRENT_DATE
    ORDER BY capture_date;
    """
    
    # Execute query and fetch results into DataFrame
    df = conn.query(query)
    
    return df

# Create the form for user input
with st.form("my_form"):
    allianceids = st.text_input("Alliance IDs (separated by commas)")
    days = st.text_input("Days")
    submit = st.form_submit_button("Submit")

if submit:
    df = ma_inf(allianceids, days)
    
    if df is not None and not df.empty:
        # Create the line graph using Plotly
        fig = px.line(df, x='capture_date', y='avg_daily_income', color='alliance_id',
                      title='Average Daily Income of Alliances Over Time',
                      labels={'capture_date': 'Date', 'avg_daily_income': 'Average Daily Income'})
        
        # Display the line graph with Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No data available for the specified criteria.")
