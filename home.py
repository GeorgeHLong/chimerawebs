import streamlit as st
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.header("Log in")

    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

create_page = st.Page("pages/Home.py", title="Home", icon=":material/home:")
delete_page = st.Page("pages/Alliance_Military_Data.py", title="Alliance Military Data", icon=":material/military_tech:")
citycalc = st.Page("pages/City_Calculator.py", title="City Build Calculator", icon=":material/apartment:")

avgcityrev= st.Page("pages/Nation_Tiering_System.py", title="Avg. City Revenue by Alliance", icon=":material/attach_money:")
alliancetiering = st.Page("pages/alliance_tiering.py", title="Alliance Tiering", icon=":material/equalizer:")
peerreport = st.Page("pages/peerreport.py", title="Alliance Tiering", icon=":material/summarize:")
cityoptimizer = st.Page("pages/cityoptimizer.py", title="City Optimizer",icon=":material/monitoring:")
beigeturn = st.Page("pages/beige_turn.py", title="Beige Sniper",icon=":material/crisis_alert:")

if st.session_state.logged_in:
    pg = st.navigation([logout_page,create_page, delete_page,citycalc,avgcityrev,peerreport,beigeturn])
else:
    pg = st.navigation([login_page])
    
st.set_page_config(page_title="Chimera Corp", page_icon="./images/chimera.png")
pg.run()