import streamlit as st
import plotly.express as px
import pandas as pd
import tabulate

# Display the banner image
st.image("images/banner.png")

# Connect to the database

# Set the title of the app
st.markdown("# Turns from Beige")
st.write("See how many turns people have left")

conn = st.connection("postgresql", type="sql")

def ma_inf(allianceids):
    # Define SQL query
    query = f"""
    select id, num_cities, score, beige_turns from tiny_nations tn where alliance_id in ({allianceids}) and beige_turns > 0 order by num_cities where tax_id != 0
    """
    
    # Execute query and fetch results into DataFrame
    df = conn.query(query)
    
    # Create the hyperlink column
    df['Nation Link'] = df['id'].apply(lambda x: f"[{x}](https://politicsandwar.com/nation/id={x})")
    
    return df

# Create the form for user input
with st.form("my_form"):
    allianceids = st.text_input("Alliance IDs")
    submit = st.form_submit_button("Submit")

if submit:
    df = ma_inf(allianceids)
    
    # Display the DataFrame with hyperlinks
    st.write(df[['Nation Link', 'num_cities', 'score', 'beige_turns']].to_markdown(index=False))
