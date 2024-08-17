import streamlit as st
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")

st.title="Nation Tiering System"

def ma_inf(allianceids):
    # Define SQL query
    query = f"""
    SELECT 
        tn.id AS "Nation ID",
        tn.nation_name AS "Nation Name",
        tn.discord AS "Discord Name",
        tn.num_cities AS "City Count",
        tn.score AS "Score",
        tn.score * 1.25 AS "Upper Target Value",
        tn.score * 0.75 AS "Lower Target Score",
        tn.soldiers AS Soldiers,
        tn.tanks AS Tanks,
        tn.aircraft AS Aircraft,
        tn.ships AS Ships,
        tn.missiles AS Missiles,
        tn.nukes AS Nukes,
        tn.spies AS Spies,
        n.vital_defense_system AS VDS,
        n.nuclear_research_facility AS NRF
    FROM tiny_nations tn
    JOIN nationprojects n ON tn.id = n.nation_id
    WHERE alliance_id IN ({allianceids})
    AND applicant = false
    AND tn.vacation_mode_turns = 0
    ORDER BY tn.num_cities DESC;
    """

    # Execute query and fetch results into DataFrame
    df = conn.query(query)


    # Display DataFrame with Streamlit
    st.write(df)

        # Run script when the button is clicked
allianceids = None
with st.form("my_form"):
    allianceids= st.text_input("Alliance IDs (separated by commas)")
    submit = st.form_submit_button("Get MA Information")
if submit:
    result = ma_inf(allianceids)
    st.write(result)