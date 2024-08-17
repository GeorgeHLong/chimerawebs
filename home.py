import streamlit as st

home = st.Page("home.py", title="Home")
citycalc = st.Page("pages/City_Calculator.py", title="City Calculator")


pg = st.navigation([home, citycalc])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()

st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
# Run a query
st.markdown("# Welcome to Chimera Corp.")