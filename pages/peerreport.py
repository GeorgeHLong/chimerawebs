import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")

# Connect to the database

# Set the title of the app
st.markdown("# Avg. City Tiering by Alliance")
st.write("Compare Alliance Tiering")

conn = st.connection("postgresql", type="sql")
def ma_inf(allianceids):
    # Define SQL query
    
    query = f"""
        SELECT a.alliancename as "Alliance Name",a.alliance_id as "Alliance ID",
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
        join alliances a 
        on a.alliance_id = tn.alliance_id 
        WHERE a.alliance_id IN ({allianceids})
        AND tax_id != 0
        AND applicant = false
        AND vacation_mode_turns = 0
        GROUP BY a.alliance_id
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
    st.write(df)
