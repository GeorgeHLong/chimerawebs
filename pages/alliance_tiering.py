import streamlit as st
import plotly.express as px
import pandas as pd
import psycopg2
from psycopg2 import sql

# Display the banner image
st.image("images/banner.png")

# Set the title of the app
st.markdown("# Avg. City Revenue by Alliance")
st.write("Find out how an alliance's city revenue changed over time and compare between alliances.")

def fetch_data(alliance_ids, days):
    # Validate input
    if not alliance_ids or not days:
        st.error("Please provide both Alliance IDs and Days.")
        return None

    # Connect to the PostgreSQL database
    try:
        conn = st.connection("postgresql", type="sql")
        cursor = conn.cursor()


        # Prepare the SQL query
        query = sql.SQL("""
        SELECT capture_date, alliance_id, (totalgdp / totalcities / 365.25) AS avg_daily_income
        FROM alliance_city_distribution
        WHERE alliance_id IN ({alliance_ids}) AND capture_date BETWEEN CURRENT_DATE - INTERVAL %s AND CURRENT_DATE
        ORDER BY capture_date;
        """).format(alliance_ids=sql.SQL(',').join(sql.Identifier(id) for id in alliance_ids.split(',')))

        cursor.execute(query, (f'{days} days',))
        results = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

        return results
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def create_plots(df):
    # Line chart for average daily income over time
    fig = px.line(df, x='capture_date', y='avg_daily_income', color='alliance_id',
                  title='Average Daily Income of Alliances Over Time',
                  labels={'capture_date': 'Date', 'avg_daily_income': 'Average Daily Income'})
    
    # Display the line chart
    st.plotly_chart(fig)

# Create the form for user input
with st.form("my_form"):
    alliance_ids = st.text_input("Alliance IDs (separated by commas)").strip()
    days = st.text_input("Days").strip()
    submit = st.form_submit_button("Get MA Information")

if submit:
    data = fetch_data(alliance_ids, days)
    
    if data:
        df = pd.DataFrame(data, columns=["capture_date", "alliance_id", "avg_daily_income"])
        create_plots(df)
    else:
        st.write("No data available for the specified criteria.")
