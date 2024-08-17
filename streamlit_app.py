import streamlit as st

def run_script(coalpower,oilpower,nuclearpower,windpower,bauxite,coal,iron,lead,oil):
    # Replace this with your actual Python script logic
    return f"Hello, {coalpower,oilpower,nuclearpower,windpower,bauxite,coal,iron,lead,oil}! Your script ran successfully."

# Streamlit app layout
st.title('Welcome to Chimera City Designer')

# Input text box
coalpower = st.text_input('Coal Power Plant')
oilpower = st.text_input('Oil Power Plant')
nuclearpower = st.text_input('Nuclear Power Plant')
windpower = st.text_input('Wind Power Plant')
bauxite = st.text_input('Bauxite Mine')
coal = st.text_input('Coal Mine')
iron = st.text_input('Iron Mine')
lead = st.text_input('Lead Mine')
oil = st.text_input('Oil Well')





# Run script when the button is clicked
if st.button('Run Script'):
    result = run_script(coalpower,oilpower,nuclearpower,windpower,bauxite,coal,iron,lead,oil)
    st.write(result)
