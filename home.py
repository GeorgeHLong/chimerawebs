import streamlit as st
st.set_page_config(page_title="Chimera Corp", page_icon="./images/chimera.png")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
conn = st.connection("postgresql", type="sql")

def login():
    # Create the form for user input
        # Display the banner image

    st.image("images/banner.png")
    with st.form("my_form"):
        username = st.text_input("Username")
        password = st.text_input("Password")
        submit = st.form_submit_button("Log in")
    if submit:
            query2 = f"""select nation_id, username, password,tn.nation_name from registeredusertable r join tiny_nations tn on tn.id = r.nation_id where username = '{username}' and password = '{password}'"""  
            results = conn.query(query2)
            # Check if the query returned any results
            if not results.empty:
                # Extract values from the first row of the DataFrame
                dbnation_id = results.at[0, 'nation_id']
                dbusername = results.at[0, 'username']
                dbpassword = results.at[0, 'password']
                dbuserdisplay = results.at[0, 'nation_name']
                
                # Display the values using Streamlit
                st.write(dbnation_id, dbusername, username, dbpassword, password)
                if dbusername == username and dbpassword == password:
                    st.session_state.logged_in = True
                    st.session_state.role = dbnation_id
                    st.session_state.nationname = dbuserdisplay

                    st.rerun()
            else:
                st.warning("Wrong username/password")





def logout():
    st.image("images/banner.png")
    st.markdown("## Log out of Chimera Web")
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
profile = st.Page("pages/profile.py", title="Profile", icon=":material/summarize:")

if st.session_state.logged_in:
    pg = st.navigation([profile,delete_page,citycalc,avgcityrev,peerreport,beigeturn,logout_page])
else:
    pg = st.navigation([create_page,login_page])
    
pg.run()