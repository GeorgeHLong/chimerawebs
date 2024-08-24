import streamlit as st
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
conn = st.connection("postgresql", type="sql")

def login():
    # Create the form for user input
        # Display the banner image
    st.set_page_config(page_title="Chimera Corp", page_icon="./images/chimera.png")

    st.image("images/banner.png")
    with st.form("my_form"):
        username = st.text_input("Username")
        password = st.text_input("Password")
        submit = st.form_submit_button("Log in")
    if submit:
            query2 = f"""select nation_id, username, "password" from registeredusertable r where username = {username} and password = {password}'"""  
            if query2 != None:      
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                st.warning("Incorrect username or password")
                

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
    pg = st.navigation([create_page, delete_page,citycalc,avgcityrev,peerreport,beigeturn,logout_page])
else:
    pg = st.navigation([login_page])
    
pg.run()