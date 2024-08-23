import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

# Define your users' names, usernames, and hashed passwords
credentials = {
    "usernames": {
        "pparker": {"name": "Peter Parker", "password": "hashed_password1"},
        "rmiller": {"name": "Rebecca Miller", "password": "hashed_password2"},
        "bharath": {"name": "Bharath", "password": "hashed_password3"}
    }
}

# Load the hashed passwords from the pickle file
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# Assign the correct hashed passwords to the credentials dictionary
for username, password in zip(credentials["usernames"], hashed_passwords):
    credentials["usernames"][username]["password"] = password

# Authentication setup
authenticator = stauth.Authenticate(credentials, "SIPL_dashboard", "abcdef")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.sidebar.title(f"Welcome {name}")
    st.write("# Welcome to Streamlit!")
    st.subheader("Introduction:")
    st.text("1. \n2. \n3. \n4. \n5. \n")
    st.sidebar.success("Select a page above.")
    
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    authenticator.logout("Logout", "sidebar")
