import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
st.connect(**st.secrets.db_credentials)

st.write("DB username:", st.secrets["username"])
st.write("DB password:", st.secrets["password"])
# Connect to the database
conn = st.connection("postgresql", type="sql")

