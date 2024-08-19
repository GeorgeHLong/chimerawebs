import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")

# Connect to the database
conn = st.connection("postgresql", type="sql")

# Set the title of the app
st.markdown("# Avg. City Tiering by Alliance")
st.write("Find how alliance's city tiering changed over time and compare between alliances")

def ma_inf(allianceids):
    # Define SQL query
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
        WHERE alliance_id = {allianceids}
        GROUP BY DATE(date)
        ORDER BY DATE(date);
    """
    
    # Execute query and fetch results into DataFrame
    df = conn.query(query)
    
    return df

# Create the form for user input
with st.form("my_form"):
    allianceids = st.text_input("Alliance ID")
    submit = st.form_submit_button("Submit")

if submit:
    df = ma_inf(allianceids)
    st.write(df)
    
    # 2. Transform the DataFrame for Plotly
    df_melted = df.melt(id_vars=["Alliance Name"], 
                        value_vars=["1-10", "11-16", "17-20", "21-25", "26-30", "31-35", "36-40", "41-45", "46-50", "50+"],
                        var_name="City Range", value_name="Count")
    # 3. Create the Plotly bar chart
    fig = px.bar(df_melted, 
                x="City Range", 
                y="Count", 
                color="Alliance Name", 
                barmode="group",
                title="City Distribution by Alliance")    
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)
