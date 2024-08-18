import streamlit as st
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")

st.title="Nation Tiering System"

def ma_inf(allianceids,days):
    # Define SQL query
    query = f"""
    SELECT capture_date, alliance_id, (totalgdp / totalcities / 365.25) AS avg_daily_income
    FROM alliance_city_distribution
    WHERE alliance_id IN {allianceids} AND capture_date BETWEEN CURRENT_DATE - INTERVAL '{days} days' AND CURRENT_DATE
    ORDER BY capture_date;
    """

    # Execute query and fetch results into DataFrame
    df = conn.query(query)


    # Display DataFrame with Streamlit
    st.write(df)

        # Run script when the button is clicked
allianceids = None
with st.form("my_form"):
    allianceids= st.text_input("Alliance IDs (separated by commas)")
    days = st.number_input("Days",min_value = 1)
    submit = st.form_submit_button("Get MA Information")
if submit:
    result = ma_inf(allianceids,days)
    st.write(result)