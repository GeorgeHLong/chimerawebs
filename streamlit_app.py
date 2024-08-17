import streamlit as st
import json

def run_script(infra_needed, imp_total, imp_coalpower, imp_oilpower, imp_windpower, imp_nuclearpower, imp_coalmine, imp_oilwell, imp_uramine, imp_leadmine, imp_ironmine, imp_bauxitemine, imp_farm, imp_gasrefinery, imp_aluminumrefinery, imp_munitionsfactory, imp_steelmill, imp_policestation, imp_hospital, imp_recyclingcenter, imp_subway, imp_supermarket, imp_bank, imp_mall, imp_stadium, imp_barracks, imp_factory, imp_hangars, imp_drydock):
    # Replace this with your actual Python script logic
    return f"Hello, {infra_needed, imp_total, imp_coalpower, imp_oilpower, imp_windpower, imp_nuclearpower, imp_coalmine, imp_oilwell, imp_uramine, imp_leadmine, imp_ironmine, imp_bauxitemine, imp_farm, imp_gasrefinery, imp_aluminumrefinery, imp_munitionsfactory, imp_steelmill, imp_policestation, imp_hospital, imp_recyclingcenter, imp_subway, imp_supermarket, imp_bank, imp_mall, imp_stadium, imp_barracks, imp_factory, imp_hangars, imp_drydock}! Your script ran successfully."

# Streamlit app layout
st.title('Welcome to Chimera City Designer')

# Input text box
data = st.text_input('City Build')


parsed_data = json.loads(data)

# Assign each value to a separate variable
infra_needed = parsed_data["infra_needed"]
imp_total = parsed_data["imp_total"]
imp_coalpower = parsed_data["imp_coalpower"]
imp_oilpower = parsed_data["imp_oilpower"]
imp_windpower = parsed_data["imp_windpower"]
imp_nuclearpower = parsed_data["imp_nuclearpower"]
imp_coalmine = parsed_data["imp_coalmine"]
imp_oilwell = parsed_data["imp_oilwell"]
imp_uramine = parsed_data["imp_uramine"]
imp_leadmine = parsed_data["imp_leadmine"]
imp_ironmine = parsed_data["imp_ironmine"]
imp_bauxitemine = parsed_data["imp_bauxitemine"]
imp_farm = parsed_data["imp_farm"]
imp_gasrefinery = parsed_data["imp_gasrefinery"]
imp_aluminumrefinery = parsed_data["imp_aluminumrefinery"]
imp_munitionsfactory = parsed_data["imp_munitionsfactory"]
imp_steelmill = parsed_data["imp_steelmill"]
imp_policestation = parsed_data["imp_policestation"]
imp_hospital = parsed_data["imp_hospital"]
imp_recyclingcenter = parsed_data["imp_recyclingcenter"]
imp_subway = parsed_data["imp_subway"]
imp_supermarket = parsed_data["imp_supermarket"]
imp_bank = parsed_data["imp_bank"]
imp_mall = parsed_data["imp_mall"]
imp_stadium = parsed_data["imp_stadium"]
imp_barracks = parsed_data["imp_barracks"]
imp_factory = parsed_data["imp_factory"]
imp_hangars = parsed_data["imp_hangars"]
imp_drydock = parsed_data["imp_drydock"]



# Run script when the button is clicked
if st.button('Run Script'):
    result = run_script(infra_needed, imp_total, imp_coalpower, imp_oilpower, imp_windpower, imp_nuclearpower, imp_coalmine, imp_oilwell, imp_uramine, imp_leadmine, imp_ironmine, imp_bauxitemine, imp_farm, imp_gasrefinery, imp_aluminumrefinery, imp_munitionsfactory, imp_steelmill, imp_policestation, imp_hospital, imp_recyclingcenter, imp_subway, imp_supermarket, imp_bank, imp_mall, imp_stadium, imp_barracks, imp_factory, imp_hangars, imp_drydock)
    st.write(result)
