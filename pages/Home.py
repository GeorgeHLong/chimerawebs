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

st.write("Welcome to Chimera Corp, your trusted partner in data analysis and strategic insights for the game Politics and War. At Chimera Corp, we specialize in transforming complex in-game data into actionable intelligence, empowering alliances and nations to make informed decisions. Whether you're looking to optimize your nation's performance, outmaneuver your rivals, or gain a competitive edge, our cutting-edge analytics and tailored solutions will help you conquer the political landscape. Join us and unlock the full potential of your nation with Chimera Corp—where data meets domination.")

st.markdown("## [Sign Up Today!](https://discord.gg/4rskMsbMtY)")
st.markdown("## Cutting-Edge Data Analysis")
st.image("images/homepage1.jpeg")
st.write("Unlock the power of data with AI-driven algorithms for game trends and player behavior insights")

st.markdown("## Empowering Orbis with Quality Effectively")
st.image("images/homepage2.jpeg")
st.write("Chimera Corp is dedicated to revolutionizing the gaming industry through cutting-edge technology. With our state-of-the-art Discord Bots, Alliance Consultancy Services, and Data Analysis tools, we provide gamers with the tools they need to excel for whatever they need. Join us and unlock a new level of gaming expertise.")

st.markdown("## AI-Driven Technology")
st.image("images/ai.jpeg")
st.write("Enhance your gameplay with AI-powered bots that streamline communication and coordination")

