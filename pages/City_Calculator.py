import streamlit as st
import json
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")

st.markdown("# City Calculator")
def run_script(ironworks,uraniumenrich,massirrigation, land,imp_total, imp_coalpower, imp_oilpower, imp_windpower, imp_nuclearpower, imp_coalmine, imp_oilwell, imp_uramine, imp_leadmine, imp_ironmine, imp_bauxitemine, imp_farm, imp_gasrefinery, imp_aluminumrefinery, imp_munitionsfactory, imp_steelmill, imp_policestation, imp_hospital, imp_recyclingcenter, imp_subway, imp_supermarket, imp_bank, imp_mall, imp_stadium, imp_barracks, imp_factory, imp_hangars, imp_drydock):
    # Replace this with your actual Python script logic
    bauxiteproduced = ((imp_bauxitemine*3)*(1+(0.5/9)*(imp_bauxitemine-1)))
    coalproduced =((imp_coalmine*3)*(1+(0.5/9)*(imp_coalmine-1)))
    ironproduced =((imp_ironmine*3)*(1+(0.5/9)*(imp_ironmine-1)))   
    leadproduced =((imp_leadmine*3)*(1+(0.5/9)*(imp_leadmine-1)))
    oilproduced = ((imp_oilwell*3)*(1+(0.5/9)*(imp_oilwell-1)))
    if uraniumenrich:
        uraniumproduced = (imp_uramine*3*(1+(0.5/4)*(imp_uramine-1))*2)
    else:
        uraniumproduced = (imp_uramine*3)*(1+(0.5/4)*(imp_uramine-1))
    if massirrigation:
        foodproduced = (imp_farm*(land/400))*12
    else:
        foodproduced = (imp_farm*(land/500))*12
    if ironworks:
        steelproduced = (imp_steelmill*12.24)*(1+0.125*(imp_steelmill-1))
    else:
        steelproduced = (imp_steelmill*9)*(1+0.125*(imp_steelmill-1))
    if emergencygas:
        gasproduced = (imp_gasrefinery*12)*(1+0.125*(imp_gasrefinery-1))
    else:
        gasproduced = (imp_gasrefinery*9)*(1+0.125*(imp_gasrefinery-1))
    if bauxiteworks:
        aluminumproduced = (imp_aluminumrefinery*12.24)*(1+0.125*(imp_aluminumrefinery-1))
    else:
        aluminumproduced = (imp_aluminumrefinery*9)*(1+0.125*(imp_aluminumrefinery-1))
        
        
    return bauxiteproduced, ironproduced, leadproduced,oilproduced, coalproduced,uraniumproduced,foodproduced,steelproduced,gasproduced,aluminumproduced

with st.form("citycalc"):
    left_column, center,right_column = st.columns(3)
    data = st.text_input('Paste City Build Template from Politics and War', '')

    with left_column:
        cityage = st.number_input("Age",step=50)
    with center:
        land = st.number_input("Land",step=500,value=1500)
    with right_column:
        infra = st.number_input("Infrastructure",step=50,value=1500)
    st.write("Projects")
    pleft_column, pright_column = st.columns(2)

    with pleft_column:
        armstockpile = st.checkbox("Arms Stockpile")
        bauxiteworks = st.checkbox("Bauxite Works")
        emergencygas = st.checkbox("Emergency Gasoline Reserve")
        ironworks = st.checkbox("Ironworks")
        uraniumenrich= st.checkbox("Uranium Enrichment Program")
        clinicalresearch = st.checkbox("Clinical Research Center")
        greentech = st.checkbox("Green Technologies")
    with pright_column:
        governmentsupport = st.checkbox("Government Support Agency")
        itc = st.checkbox("International Trade Center")
        massirrigation = st.checkbox("Mass Irrigation")
        recycling = st.checkbox("Recycling Initiative")
        policeprogram = st.checkbox("Specialized Police Training Program")
        telesat = st.checkbox("Telecom Satellite")
        openmarkets = st.checkbox("Open Markets")
    submit = st.form_submit_button('Submit')
if submit:    
    if data:
        try:
            parsed_data = json.loads(data)
            infra_needed = parsed_data.get("infra_needed", 0)
            imp_total = parsed_data.get("imp_total", 0)
            imp_coalpower = parsed_data.get("imp_coalpower", 0)
            imp_oilpower = parsed_data.get("imp_oilpower", 0)
            imp_windpower = parsed_data.get("imp_windpower", 0)
            imp_nuclearpower = parsed_data.get("imp_nuclearpower", 0)
            imp_coalmine = parsed_data.get("imp_coalmine", 0)
            imp_oilwell = parsed_data.get("imp_oilwell", 0)
            imp_uramine = parsed_data.get("imp_uramine", 0)
            imp_leadmine = parsed_data.get("imp_leadmine", 0)
            imp_ironmine = parsed_data.get("imp_ironmine", 0)
            imp_bauxitemine = parsed_data.get("imp_bauxitemine", 0)
            imp_farm = parsed_data.get("imp_farm", 0)
            imp_gasrefinery = parsed_data.get("imp_gasrefinery", 0)
            imp_aluminumrefinery = parsed_data.get("imp_aluminumrefinery", 0)
            imp_munitionsfactory = parsed_data.get("imp_munitionsfactory", 0)
            imp_steelmill = parsed_data.get("imp_steelmill", 0)
            imp_policestation = parsed_data.get("imp_policestation", 0)
            imp_hospital = parsed_data.get("imp_hospital", 0)
            imp_recyclingcenter = parsed_data.get("imp_recyclingcenter", 0)
            imp_subway = parsed_data.get("imp_subway", 0)
            imp_supermarket = parsed_data.get("imp_supermarket", 0)
            imp_bank = parsed_data.get("imp_bank", 0)
            imp_mall = parsed_data.get("imp_mall", 0)
            imp_stadium = parsed_data.get("imp_stadium", 0)
            imp_barracks = parsed_data.get("imp_barracks", 0)
            imp_factory = parsed_data.get("imp_factory", 0)
            imp_hangars = parsed_data.get("imp_hangars", 0)
            imp_drydock = parsed_data.get("imp_drydock", 0)
            result = run_script(ironworks,uraniumenrich,massirrigation, land,imp_total, imp_coalpower, imp_oilpower, imp_windpower, imp_nuclearpower, imp_coalmine, imp_oilwell, imp_uramine, imp_leadmine, imp_ironmine, imp_bauxitemine, imp_farm, imp_gasrefinery, imp_aluminumrefinery, imp_munitionsfactory, imp_steelmill, imp_policestation, imp_hospital, imp_recyclingcenter, imp_subway, imp_supermarket, imp_bank, imp_mall, imp_stadium, imp_barracks, imp_factory, imp_hangars, imp_drydock)
            st.write(result)
        except json.JSONDecodeError as e:
            st.error(f"JSON decode error: {e}")
    else:
        st.warning("Please provide valid city build data.")


