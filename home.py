import streamlit as st

create_page = st.Page("pages/Home.py", title="Home", icon=":material/home:")
delete_page = st.Page("pages/Alliance_Military_Data.py", title="Alliance Military Data", icon=":material/analytics:")
citycalc = st.Page("pages/City_Calculator.py", title="City Build Calculator", icon=":material/apartment:")

avgcityrev= st.Page("pages/Nation_Tiering_System.py", title="Avg. City Revenue by Alliance", icon=":material/attach_money:")
alliancetiering = st.Page("pages/alliance_tiering.py", title="Alliance Tiering", icon=":material/apartment:")
peerreport = st.Page("pages/peerreport.py", title="Peer Report", icon=":material/summarize:")


pg = st.navigation([create_page, delete_page,citycalc,avgcityrev,peerreport])
st.set_page_config(page_title="Chimera Corp", page_icon="./images/chimera.png")
pg.run()