import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")

st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])
# Connect to the database
conn = st.connection("postgresql", type="sql")

