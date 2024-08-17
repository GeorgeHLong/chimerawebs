import streamlit as st

create_page = st.Page("pages/Home.py", title="Home", icon=":material/add_circle:")
delete_page = st.Page("pages/Alliance_Military_Data.py", title="Alliance Military Data", icon=":material/delete:")

pg = st.navigation([create_page, delete_page])
st.set_page_config(page_title="Chimera Corp", page_icon="/images/chimera.png")
pg.run()