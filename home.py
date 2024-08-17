import streamlit as st

home = st.Page("pages/home.py", title="Home Page")
citycalc = st.Page("pages/City_Calculator.py", title="City Calculator")


pg = st.navigation([home, citycalc])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()