import streamlit as st

def run_script(user_input):
    # Replace this with your actual Python script logic
    return f"Hello, {user_input}! Your script ran successfully."

# Streamlit app layout
st.title('Run Python Script')

# Input text box
user_input = st.text_input('Enter some text:')

# Run script when the button is clicked
if st.button('Run Script'):
    result = run_script(user_input)
    st.write(result)
