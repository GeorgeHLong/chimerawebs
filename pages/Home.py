import streamlit as st

import json
import pandas as pd 
import numpy as np
import time
from pathlib import Path

import plotly.express as px  # pip install plotly-express
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
# Run a query

nationid = "admin"
password = "admin"
query2 = f"""
    select nation_id,username, password from registeredusertable where username = '{nationid}' and password = '{password}'
    """
value = conn.query(query2)
if not value.empty:
    nationid = value.loc[0, 'nation_id']
    username = value.loc[0, 'username']
    password = value.loc[0, 'password']
    nationid = str(nationid)
    info = zip(nationid, username, password)
    
    st.write(info)
else:
    st.write("No data found for the given query.")

authenticator = stauth.Authenticate(nationid, username, password,"SIPL_dashboard", "abcdef")
name, authentication_status, username = authenticator.login("Login", "main")

    
st.write("Welcome to Chimera Corp, your trusted partner in data analysis and strategic insights for the game Politics and War. At Chimera Corp, we specialize in transforming complex in-game data into actionable intelligence, empowering alliances and nations to make informed decisions. Whether you're looking to optimize your nation's performance, outmaneuver your rivals, or gain a competitive edge, our cutting-edge analytics and tailored solutions will help you conquer the political landscape. Join us and unlock the full potential of your nation with Chimera Corp—where data meets domination.")

st.markdown("## Cutting-Edge Data Analysis")
st.image("images/homepage1.jpeg",)
st.write("Unlock the power of data with AI-driven algorithms for game trends and player behavior insights")

st.markdown("## Empowering Orbis with Quality Effectively")
st.image("images/homepage2.jpeg",)
st.write("Chimera Corp is dedicated to revolutionizing the gaming industry through cutting-edge technology. With our state-of-the-art Discord Bots, Alliance Consultancy Services, and Data Analysis tools, we provide gamers with the tools they need to excel for whatever they need. Join us and unlock a new level of gaming expertise.")


st.markdown("## AI-Driven Technology")
st.image("images/ai.jpeg",)
st.write("Enhance your gameplay with AI-powered bots that streamline communication and coordination")



