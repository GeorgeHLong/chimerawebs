import streamlit as st
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")

st.title="City Calculator"