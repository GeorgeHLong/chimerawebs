import streamlit as st
import json
import numpy as np
import pandas as pd
import plotly.express as px

import math
st.image("images/banner.png")
conn = st.connection("postgresql", type="sql")

st.markdown("# City Calculator")
def run_script(parsed_data,infra,land,armstockpile,bauxiteworks,emergencygas,ironworks,uraniumenrich,clinicalresearch,greentech,governmentsupport,itc,massirrigation,recycling,policeprogram,telesat,openmarkets):
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
    # Replace this with your actual Python script logic
    # Production calculations
    bauxiteproduced = ((imp_bauxitemine * 3) * (1 + (0.5 / 9) * (imp_bauxitemine - 1)))
    coalproduced = ((imp_coalmine * 3) * (1 + (0.5 / 9) * (imp_coalmine - 1)))
    ironproduced = ((imp_ironmine * 3) * (1 + (0.5 / 9) * (imp_ironmine - 1)))
    leadproduced = ((imp_leadmine * 3) * (1 + (0.5 / 9) * (imp_leadmine - 1)))
    oilproduced = ((imp_oilwell * 3) * (1 + (0.5 / 9) * (imp_oilwell - 1)))
    uraniumproduced = (imp_uramine * 3 * (1 + (0.5 / 4) * (imp_uramine - 1))) * (2 if uraniumenrich else 1)
    foodproduced = (imp_farm * (land / (400 if massirrigation else 500))) * 12
    steelmultiplier = 12.24 if ironworks else 9
    steelproduced = (imp_steelmill * steelmultiplier) * (1 + 0.125 * (imp_steelmill - 1))
    gasmultiplier = 12 if emergencygas else 9
    gasproduced = (imp_gasrefinery * gasmultiplier) * (1 + 0.125 * (imp_gasrefinery - 1))
    aluminummultiplier = 12.24 if bauxiteworks else 9
    aluminumproduced = round((imp_aluminumrefinery * aluminummultiplier) * (1 + 0.125 * (imp_aluminumrefinery - 1)), 2)
    munitionsmultiplier = 24.12 if armstockpile else 18
    munitionsproduced = (imp_munitionsfactory * munitionsmultiplier) * (1 + 0.125 * (imp_munitionsfactory - 1))
    # Pollution index calculation
    pollutionidx = (
        imp_coalpower * 8 + imp_oilpower * 6 + imp_bauxitemine * 12 + imp_coalmine * 12 + imp_ironmine * 12 + 
        imp_leadmine * 12 + imp_oilwell * 12 + imp_uramine * 20 + (imp_farm * (1 if greentech else 2)) + 
        (imp_gasrefinery * (24 if greentech else 32)) + (imp_aluminumrefinery * (30 if greentech else 40)) + 
        (imp_steelmill * (30 if greentech else 40)) + (imp_munitionsfactory * (24 if greentech else 32)) + 
        imp_policestation * 1 + imp_hospital * 4 + (imp_recyclingcenter * (-75 if recycling else -70)) + 
        (imp_subway * (-70 if greentech else -45)) + imp_mall * 2 + imp_stadium * 5
    )
    pollutionidx = max(pollutionidx, 0)
    # Disease calculation
    basepopulation = infra * 100
    popdensity = basepopulation / land
    diseasemultiplier = 3.5 if clinicalresearch else 2.5
    disease = round(
        ((((popdensity**2) * 0.01) - 25) / 100) + (basepopulation / 100000) + (pollutionidx * 0.05) - 
        imp_hospital * diseasemultiplier, 2
    )
    # Commerce revenue calculation
    if telesat and not itc:
        st.error("You must have International Trade Center and Telecommunications Satellite to use Telecommunications Satellite")
        return None
    total_commerce = imp_supermarket * 3 + imp_bank * 5 + imp_mall * 9 + imp_stadium * 12 + imp_subway * 8
    commerce_bonus = 2 if telesat and itc else 0
    
    commercerev = round((((min(total_commerce + commerce_bonus, 125) / 50) * 0.725) + 0.725) * basepopulation, 2)
    commercerev = commercerev * 1.015 if openmarkets and governmentsupport else commercerev * 1.01 if openmarkets else commercerev
    #consumption
    cbauxx = 4.08 if bauxiteworks else 3
    cbaux = (imp_aluminumrefinery* cbauxx)*(1+0.125*(imp_aluminumrefinery-1))
    ccoalx = 4.08 if ironworks else 3
    ccoal = ((((ccoalx * imp_steelmill) * (1 + 0.125 * (imp_steelmill - 1))))+ (1.2 * math.ceil(infra / 1000) * 1000 / 100 if imp_coalpower > 0 else 0))
    cironx = 4.08 if imp_steelmill else 3
    ciron = (imp_steelmill* cironx)*(1+0.125*(imp_steelmill-1))
    cleadx = 8.04 if armstockpile else 6
    clead = (imp_munitionsfactory* cleadx)*(1+0.125*(imp_munitionsfactory-1))    
    coilx = 6 if ironworks else 3
    coil = ((((coilx * imp_gasrefinery) * (1 + 0.125 * (imp_gasrefinery - 1))))+ (1.2 * math.ceil(infra / 1000) * 1000 / 100 if imp_oilpower > 0 else 0))
    curanium = (1.2 * math.ceil(infra / 1000) * 1000 / 100 if imp_nuclearpower > 0 else 0)
    cfood = (((basepopulation**2) / 125000000) + ((basepopulation * (1 + max(math.log(cityage)/15, 0)) - basepopulation) / 850))
    # Database query
    query = """
    SELECT Food, Coal, Oil, Uranium, Bauxite, Lead, Gasoline, Munitions, Aluminum, Steel, Iron
    FROM tradeprices
    ORDER BY trade_timestamp DESC
    LIMIT 1
    """
    df = conn.query(query)
# Assuming df has only one row (due to LIMIT 1 in the query)
    if not df.empty:
        row = df.iloc[0]
        food_price = row['food']
        coal_price = row['coal']
        oil_price = row['oil']
        uranium_price = row['uranium']
        bauxite_price = row['bauxite']
        lead_price = row['lead']
        gasoline_price = row['gasoline']
        munitions_price = row['munitions']
        aluminum_price = row['aluminum']
        steel_price = row['steel']
        iron_price = row['iron']
        rss_prices = [int(item) if isinstance(item, np.integer) else float(item) for item in row]
        food_price,coal_price,oil_price,uranium_price,bauxite_price,lead_price,gasoline_price,munitions_price,aluminum_price,steel_price,iron_price = rss_prices
        rssrevenue = (
            ((foodproduced - cfood) * food_price) +
            ((coalproduced - ccoal) * coal_price) +
            ((oilproduced - coil) * oil_price) +
            ((ironproduced - ciron) * iron_price) +
            ((uraniumproduced - curanium) * uranium_price) +
            ((bauxiteproduced - cbaux) * bauxite_price) +
            ((leadproduced - clead) * lead_price) +
            ((gasproduced ) * gasoline_price) +
            ((munitionsproduced) * munitions_price) +
            ((aluminumproduced ) * aluminum_price) +
            ((steelproduced ) * steel_price)
        )
        netfood = foodproduced-cfood
        netcoal = coalproduced-ccoal
        netoil = oilproduced - coil
        netiron = ironproduced- ciron
        neturanium = uraniumproduced - curanium
        netbauxite = bauxiteproduced - cbaux
        netlead = leadproduced- clead
        
                
    else:
        food_price = coal_price = oil_price = uranium_price = bauxite_price = lead_price = gasoline_price = munitions_price = aluminum_price = steel_price = None
    return (
            netfood,netcoal,netoil,netiron,neturanium,netbauxite,netlead,cfood,ccoal,coil,curanium,cbaux,clead,rssrevenue,food_price,coal_price,oil_price,uranium_price,bauxite_price,lead_price,gasoline_price,munitions_price,aluminum_price,steel_price,commercerev, disease, 
        pollutionidx, bauxiteproduced, ironproduced, leadproduced, oilproduced, coalproduced, uraniumproduced, 
        foodproduced, steelproduced, gasproduced, aluminumproduced, munitionsproduced
    )
with st.form("citycalc"):
    left_column, center,right_column = st.columns(3)
    data = st.text_input('Paste City Build Template from Politics and War', '')
    with left_column:
        cityage = st.number_input("Age",min_value=1,step=50)
    with center:
        infra = st.number_input("Infrastructure",step=50,value=1500,min_value = 0.00001)

    with right_column:
        land = st.number_input("Land",step=500,value=1500,min_value = 0.00001)
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
            result = run_script(parsed_data,infra,land,armstockpile,bauxiteworks,emergencygas,ironworks,uraniumenrich,clinicalresearch,greentech,governmentsupport,itc,massirrigation,recycling,policeprogram,telesat,openmarkets)
            with st.container():
                netfood,netcoal,netoil,netiron,neturanium,netbauxite,netlead,cfood, ccoal, coil, curanium, cbaux, clead,rssrevenue,food_price,coal_price,oil_price,uranium_price,bauxite_price,lead_price,gasoline_price,munitions_price,aluminum_price,steel_price,commercerev, disease, pollutionidx, bauxiteproduced, ironproduced, leadproduced, oilproduced, coalproduced, uraniumproduced, foodproduced, steelproduced, gasproduced, aluminumproduced, munitionsproduced = result
                st.markdown("## Estimated Revenue")
                left_column,right_column = st.columns(2)
                with left_column:
                    st.markdown("### Raw Resources:")
                    st.write(f"Coal: {netcoal:,.2f}")
                    st.write(f"Oil: {netoil:,.2f}")
                    st.write(f"Uranium: {neturanium:,.2f}")
                    st.write(f"Lead: {netlead:,.2f}")
                    st.write(f"Iron: {netiron:,.2f}")
                    st.write(f"Bauxite: {netbauxite:,.2f}")
                    st.write(f"Food: {foodproduced:,.2f}")
                with right_column:
                    st.markdown("### Manufactured Resources:")
                    st.write(f"Gasoline: {gasproduced:,.2f}")
                    st.write(f"Munitions: {munitionsproduced:,.2f}")
                    st.write(f"Steel: {steelproduced:,.2f}")
                    st.write(f"Aluminum: {aluminumproduced:,.2f}")
                st.divider()               
                st.write(f"Est. Commerce Revenue: ${commercerev:,.2f}")
                st.write(f"Est Resource Revenue: ${rssrevenue:,.2f}")
                totalrevenue = commercerev + rssrevenue
                st.divider()
                st.write(f"Est. Total Revenue/Day: ${totalrevenue:,.2f}")
                # Data for the pie chart
                foodrev = ((foodproduced - cfood) * food_price) 
                coalrev = ((coalproduced - ccoal) * coal_price) 
                oilrev = ((oilproduced - coil) * oil_price) 
                uraniumrev = ((uraniumproduced - curanium) * uranium_price) 
                bauxiterev = ((bauxiteproduced - cbaux) * bauxite_price) 
                leadrev = ((leadproduced - clead) * lead_price) 
                gasrev = ((gasproduced) * gasoline_price) 
                munitionsrev = ((munitionsproduced) * munitions_price) 
                aluminumrev = ((aluminumproduced) * aluminum_price) 
                steelrev = ((steelproduced) * steel_price)
                netrev = foodrev+ coalrev+ oilrev+ uraniumrev+ bauxiterev+ leadrev+ gasrev+ munitionsrev+ aluminumrev+ steelrev+commercerev
                netrev = round(netrev,2)
                foodrev = round(foodrev,2)
                # Data for the pie chart
                labels = ['Food', 'Coal', 'Oil', 'Uranium', 'Bauxite', 'Lead', 'Gasoline', 'Munitions', 'Aluminum', 'Steel','Commerce','Net Revenue']
                values = [foodrev, coalrev, oilrev, uraniumrev, bauxiterev, leadrev, gasrev, munitionsrev, aluminumrev, steelrev,commercerev,netrev]

                # Create DataFrame
                df = pd.DataFrame({
                    'Resource': labels,
                    'Revenue': values
                })
                # Create a pie chart
                fig = px.bar(df, x='Resource', y='Revenue', title='Income by Revenue Source')
                fig.update_layout(
                    yaxis_tickprefix="$",
                    yaxis_tickformat=","
                )
                # Streamlit app
                st.plotly_chart(fig, use_container_width=True)        
        except json.JSONDecodeError as e:
            st.error(f"JSON decode error: {e}")
    else:
        st.error("Please provide valid city build data.")


