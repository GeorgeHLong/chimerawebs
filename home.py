import streamlit as st
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import pickle
from pathlib import Path
create_page = st.Page("pages/Home.py", title="Home", icon=":material/home:")
delete_page = st.Page("pages/Alliance_Military_Data.py", title="Alliance Military Data", icon=":material/military_tech:")
citycalc = st.Page("pages/City_Calculator.py", title="City Build Calculator", icon=":material/apartment:")

avgcityrev= st.Page("pages/Nation_Tiering_System.py", title="Avg. City Revenue by Alliance", icon=":material/attach_money:")
alliancetiering = st.Page("pages/alliance_tiering.py", title="Alliance Tiering", icon=":material/equalizer:")
peerreport = st.Page("pages/peerreport.py", title="Alliance Tiering", icon=":material/summarize:")
cityoptimizer = st.Page("pages/cityoptimizer.py", title="City Optimizer",icon=":material/monitoring:")
beigeturn = st.Page("pages/beige_turn.py", title="Beige Sniper",icon=":material/crisis_alert:")
# Define your users' names, usernames, and plaintext passwords
names = ["Peter Parker", "Rebecca Miller", "Bharath"]
usernames = ["pparker", "rmiller", "bharath"]
passwords = ["password1", "password2", "1234"]  # Replace with actual passwords

# Generate hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()
hide_bar= """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""

# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller","bharath"]
usernames = ["pparker", "rmiller","bharath"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "SIPL_dashboard", "abcdef")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    st.markdown(hide_bar, unsafe_allow_html=True)

if authentication_status == None:
    st.warning("Please enter your username and password")
    st.markdown(hide_bar, unsafe_allow_html=True)


if authentication_status:
    # # ---- SIDEBAR ----
    st.sidebar.title(f"Welcome {name}")
    # st.sidebar.header("select page here :")
    st.write("# Welcome to Streamlit!..")

    ###about ....
    st.subheader("Introduction :")
    st.text("1. \n2. \n3. \n4. \n5. \n")

    st.sidebar.success("Select a page above.")

    ###---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


    authenticator.logout("Logout", "sidebar")
pg = st.navigation([create_page, delete_page,citycalc,avgcityrev,peerreport,beigeturn])
st.set_page_config(page_title="Chimera Corp", page_icon="./images/chimera.png")
pg.run()