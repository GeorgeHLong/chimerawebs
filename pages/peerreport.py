import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
st.write("DB username:", st.secrets["db_credentials"]["username"])
st.write("DB password:", st.secrets["db_credentials"]["password"])

