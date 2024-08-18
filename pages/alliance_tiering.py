import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")

# Connect to the database

def fetch_data(alliance_id):
    # Establish a connection to the database
    conn = st.connection("postgresql", type="sql")

    # Prepare the SQL query
    query = f"""
        SELECT
            DATE(date) AS date,
            SUM("1_10") AS "1-10",
            SUM("11_16") AS "11-16",
            SUM("17_20") AS "17-20",
            SUM("21_25") AS "21-25",
            SUM("26_30") AS "26-30",
            SUM("31_35") AS "31-35",
            SUM("36_40") AS "36-40",
            SUM("41_45") AS "41-45",
            SUM("46_50") AS "46-50",
            SUM("50_plus") AS "50+"
        FROM alliancechange
        WHERE alliance_id = {alliance_id}
        GROUP BY DATE(date)
        ORDER BY DATE(date);
    """

    results = conn.query(query)

    return results


def create_plots(df):
    # Line chart for city counts over time
    fig_line = px.line(df, x='date', y=df.columns[1:], title=f"City Counts Over Time for Alliance ID: {alliance_id}",
                       labels={'date': 'Date', 'value': 'City Count'})
    
    # Display the line chart
    st.plotly_chart(fig_line)
    
    # Create table plot
    fig_table = px.imshow(df, text_auto=True, title="City Counts Table")
    
    # Display the table
    st.plotly_chart(fig_table)

# User input
alliance_id = st.text_input("Enter Alliance ID")
if st.button("Get Data"):
    if alliance_id:
        data = fetch_data(alliance_id)
        if data:
            df = pd.DataFrame(data, columns=["date", "1-10", "11-16", "17-20", "21-25", "26-30", "31-35", "36-40", "41-45", "46-50", "50+"])
            create_plots(df)
        else:
            st.write("No data found for the specified alliance.")
    else:
        st.write("Please enter an Alliance ID.")