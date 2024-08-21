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
        SELECT a.alliancename as "Alliance Name", a.alliance_id as "Alliance ID",
            COUNT(CASE WHEN num_cities BETWEEN 0 AND 10 THEN 1 END) AS "1-10",
            COUNT(CASE WHEN num_cities BETWEEN 11 AND 16 THEN 1 END) AS "11-16",
            COUNT(CASE WHEN num_cities BETWEEN 17 AND 20 THEN 1 END) AS "17-20",
            COUNT(CASE WHEN num_cities BETWEEN 21 AND 25 THEN 1 END) AS "21-25",
            COUNT(CASE WHEN num_cities BETWEEN 26 AND 30 THEN 1 END) AS "26-30",
            COUNT(CASE WHEN num_cities BETWEEN 31 AND 35 THEN 1 END) AS "31-35",
            COUNT(CASE WHEN num_cities BETWEEN 36 AND 40 THEN 1 END) AS "36-40",
            COUNT(CASE WHEN num_cities BETWEEN 41 AND 45 THEN 1 END) AS "41-45",
            COUNT(CASE WHEN num_cities BETWEEN 46 AND 50 THEN 1 END) AS "46-50",
            COUNT(CASE WHEN num_cities > 50 THEN 1 END) AS "50+"
        FROM tiny_nations tn
        JOIN alliances a 
        ON a.alliance_id = tn.alliance_id 
        WHERE a.alliance_id IN (4567, 790)
        AND tax_id != 0
        AND applicant = false
        AND vacation_mode_turns = 0
        GROUP BY a.alliance_id
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