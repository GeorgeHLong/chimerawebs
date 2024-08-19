import streamlit as st
import plotly.express as px
import pandas as pd

# Display the banner image
st.image("images/banner.png")
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])


st.write("DB username:", st.secrets["db_credentials"]["username"])
st.write("DB password:", st.secrets["db_credentials"]["password"])

