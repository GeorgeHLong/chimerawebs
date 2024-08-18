import streamlit as st

import json
import pandas as pd 
import numpy as np
import time


st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")
# Run a query

st.write("Welcome to Chimera Corp, your trusted partner in data analysis and strategic insights for the game Politics and War. At Chimera Corp, we specialize in transforming complex in-game data into actionable intelligence, empowering alliances and nations to make informed decisions. Whether you're looking to optimize your nation's performance, outmaneuver your rivals, or gain a competitive edge, our cutting-edge analytics and tailored solutions will help you conquer the political landscape. Join us and unlock the full potential of your nation with Chimera Corp—where data meets domination.")
st.image("images/homepage1.jpeg",)

st.markdown("## Cutting-Edge Data Analysis")
st.write("Unlock the power of data with AI-driven algorithms for game trends and player behavior insights")

st.image("images/homepage2.jpeg",)

st.markdown("## Empowering Orbis with Quality Effectively")
st.write("Chimera Corp is dedicated to revolutionizing the gaming industry through cutting-edge technology. With our state-of-the-art Discord Bots, Alliance Consultancy Services, and Data Analysis tools, we provide gamers with the tools they need to excel for whatever they need. Join us and unlock a new level of gaming expertise.")

st.markdown("## AI-Driven Technology")
st.write("Enhance your gameplay with AI-powered bots that streamline communication and coordination")








# Streamlit app layout
#st.title('City Calculator')

left_column, right_column = st.columns(2)
#data = st.text_input('City Build', '')

#with left_column:
    #cityage = st.text_input('Age','')
    #land = st.text_input('Land','')
#with right_column:
 #   infra = st.text_input('Infrastructure','')



# Process input only if data is provided
#if data:
  #  try:
        # Parse the JSON string into a Python dictionary
 #       parsed_data = json.loads(data)
        # Assign each value to a separate variable
   #      infra_needed = parsed_data.get("infra_needed", 0)
     #    imp_total = parsed_data.get("imp_total", 0)
       #  imp_coalpower = parsed_data.get("imp_coalpower", 0)
        # imp_oilpower = parsed_data.get("imp_oilpower", 0)
        # imp_windpower = parsed_data.get("imp_windpower", 0)
        # imp_nuclearpower = parsed_data.get("imp_nuclearpower", 0)
        #  imp_coalmine = parsed_data.get("imp_coalmine", 0)
        # imp_oilwell = parsed_data.get("imp_oilwell", 0)
        # imp_uramine = parsed_data.get("imp_uramine", 0)
       #  imp_leadmine = parsed_data.get("imp_leadmine", 0)
       #  imp_ironmine = parsed_data.get("imp_ironmine", 0)
        # imp_bauxitemine = parsed_data.get("imp_bauxitemine", 0)
        # imp_farm = parsed_data.get("imp_farm", 0)
        # imp_gasrefinery = parsed_data.get("imp_gasrefinery", 0)
        # imp_aluminumrefinery = parsed_data.get("imp_aluminumrefinery", 0)
        # imp_munitionsfactory = parsed_data.get("imp_munitionsfactory", 0)
        # imp_steelmill = parsed_data.get("imp_steelmill", 0)
        # imp_policestation = parsed_data.get("imp_policestation", 0)
        # imp_hospital = parsed_data.get("imp_hospital", 0)
        # imp_recyclingcenter = parsed_data.get("imp_recyclingcenter", 0)
        # imp_subway = parsed_data.get("imp_subway", 0)
        # imp_supermarket = parsed_data.get("imp_supermarket", 0)
        # imp_bank = parsed_data.get("imp_bank", 0)
        # imp_mall = parsed_data.get("imp_mall", 0)
        # imp_stadium = parsed_data.get("imp_stadium", 0)
        # imp_barracks = parsed_data.get("imp_barracks", 0)
        # imp_factory = parsed_data.get("imp_factory", 0)
        # imp_hangars = parsed_data.get("imp_hangars", 0)
        # imp_drydock = parsed_data.get("imp_drydock", 0)
        

        # Run script when the button is clicked
       #  if st.button('Run Script'):
            # result = run_script(infra_needed, imp_total, imp_coalpower, imp_oilpower, imp_windpower, imp_nuclearpower, imp_coalmine, imp_oilwell, imp_uramine, imp_leadmine, imp_ironmine, imp_bauxitemine, imp_farm, imp_gasrefinery, imp_aluminumrefinery, imp_munitionsfactory, imp_steelmill, imp_policestation, imp_hospital, imp_recyclingcenter, imp_subway, imp_supermarket, imp_bank, imp_mall, imp_stadium, imp_barracks, imp_factory, imp_hangars, imp_drydock)
            # st.write(result)
    # except json.JSONDecodeError as e:
        # st.error(f"JSON decode error: {e}")
# else:
    # st.warning("Please provide valid JSON data.")
