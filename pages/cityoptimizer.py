import streamlit as st
import json
import pandas as pd
import plotly.express as px
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpInteger, LpBinary

# Function to run optimization
def optimize_city_build(infra, land, armstockpile, bauxiteworks, emergencygas, ironworks, uraniumenrich, clinicalresearch, greentech, governmentsupport, itc, massirrigation, recycling, policeprogram, telesat, openmarkets):
    # Create a linear programming problem
    problem = LpProblem("CityBuildOptimization", LpMaximize)

    # Decision Variables
    imp_coalmine = LpVariable("CoalMine", lowBound=0, upBound=10, cat=LpInteger)
    imp_oilwell = LpVariable("OilWell", lowBound=0, upBound=10, cat=LpInteger)
    imp_uramine = LpVariable("UraniumMine", lowBound=0, upBound=5, cat=LpInteger)
    imp_leadmine = LpVariable("LeadMine", lowBound=0, upBound=10, cat=LpInteger)
    imp_ironmine = LpVariable("IronMine", lowBound=0, upBound=10, cat=LpInteger)
    imp_bauxitemine = LpVariable("BauxiteMine", lowBound=0, upBound=10, cat=LpInteger)
    imp_farm = LpVariable("Farm", lowBound=0, upBound=20, cat=LpInteger)
    imp_gasrefinery = LpVariable("GasRefinery", lowBound=0, upBound=5, cat=LpInteger)
    imp_aluminumrefinery = LpVariable("AluminumRefinery", lowBound=0, upBound=5, cat=LpInteger)
    imp_munitionsfactory = LpVariable("MunitionsFactory", lowBound=0, upBound=5, cat=LpInteger)
    imp_steelmill = LpVariable("SteelMill", lowBound=0, upBound=5, cat=LpInteger)
    imp_policestation = LpVariable("PoliceStation", lowBound=0, upBound=5, cat=LpInteger)
    imp_hospital = LpVariable("Hospital", lowBound=0, upBound=5, cat=LpInteger)
    imp_recyclingcenter = LpVariable("RecyclingCenter", lowBound=0, upBound=3, cat=LpInteger)
    imp_subway = LpVariable("Subway", lowBound=0, upBound=5, cat=LpInteger)
    imp_supermarket = LpVariable("Supermarket", lowBound=0, upBound=5, cat=LpInteger)
    imp_bank = LpVariable("Bank", lowBound=0, upBound=5, cat=LpInteger)
    imp_mall = LpVariable("Mall", lowBound=0, upBound=5, cat=LpInteger)
    imp_stadium = LpVariable("Stadium", lowBound=0, upBound=5, cat=LpInteger)

    # Binary decision variables for upgrades
    uraniumenrich = LpVariable("UraniumEnrichment", cat=LpBinary)
    armstockpile = LpVariable("ArmsStockpile", cat=LpBinary)
    bauxiteworks = LpVariable("BauxiteWorks", cat=LpBinary)
    emergencygas = LpVariable("EmergencyGasReserve", cat=LpBinary)
    ironworks = LpVariable("IronWorks", cat=LpBinary)
    clinicalresearch = LpVariable("ClinicalResearch", cat=LpBinary)
    greentech = LpVariable("GreenTech", cat=LpBinary)
    governmentsupport = LpVariable("GovernmentSupport", cat=LpBinary)
    itc = LpVariable("ITC", cat=LpBinary)
    massirrigation = LpVariable("MassIrrigation", cat=LpBinary)
    recycling = LpVariable("RecyclingProgram", cat=LpBinary)
    policeprogram = LpVariable("PoliceProgram", cat=LpBinary)
    telesat = LpVariable("TelecommunicationsSatellite", cat=LpBinary)
    openmarkets = LpVariable("OpenMarkets", cat=LpBinary)

    # Calculations
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

    pollutionidx = (
        imp_coalmine * 12 + imp_oilwell * 12 + imp_bauxitemine * 12 + imp_leadmine * 12 + imp_ironmine * 12 +
        imp_uramine * 20 + (imp_farm * (1 if greentech else 2)) + 
        (imp_gasrefinery * (24 if greentech else 32)) + (imp_aluminumrefinery * (30 if greentech else 40)) + 
        (imp_steelmill * (30 if greentech else 40)) + (imp_munitionsfactory * (24 if greentech else 32)) + 
        imp_policestation * 1 + imp_hospital * 4 + (imp_recyclingcenter * (-75 if recycling else -70)) + 
        (imp_subway * (-70 if greentech else -45)) + imp_mall * 2 + imp_stadium * 5
    )
    pollutionidx = max(pollutionidx, 0)

    basepopulation = infra * 100
    popdensity = basepopulation / land
    diseasemultiplier = 3.5 if clinicalresearch else 2.5
    disease = round(
        ((((popdensity**2) * 0.01) - 25) / 100) + (basepopulation / 100000) + (pollutionidx * 0.05) - 
        imp_hospital * diseasemultiplier, 2
    )

    if telesat and not itc:
        st.error("You must have International Trade Center and Telecommunications Satellite to use Telecommunications Satellite")
        return None
    total_commerce = imp_supermarket * 3 + imp_bank * 5 + imp_mall * 9 + imp_stadium * 12 + imp_subway * 8
    commerce_bonus = 2 if telesat and itc else 0
    
    commercerev = round((((min(total_commerce + commerce_bonus, 125) / 50) * 0.725) + 0.725) * basepopulation, 2)
    commercerev = commercerev * 1.015 if openmarkets and governmentsupport else commercerev * 1.01 if openmarkets else commercerev

    rssrevenue = (
        ((foodproduced) * 5) +
        ((coalproduced) * 5) +
        ((oilproduced) * 5) +
        ((ironproduced) * 5) +
        ((uraniumproduced) * 5) +
        ((bauxiteproduced) * 5) +
        ((leadproduced) * 5) +
        ((gasproduced) * 5) +
        ((munitionsproduced) * 5) +
        ((aluminumproduced) * 5) +
        ((steelproduced) * 5)
    )
    
    revenue = round(rssrevenue + commercerev, 2)
    
    # Objective: Maximize revenue
    problem += revenue

    # Constraints
    problem += (imp_coalmine + imp_oilwell + imp_uramine + imp_leadmine + imp_ironmine + imp_bauxitemine + imp_farm + imp_gasrefinery + imp_aluminumrefinery + imp_munitionsfactory + imp_steelmill + imp_policestation + imp_hospital + imp_recyclingcenter + imp_subway + imp_supermarket + imp_bank + imp_mall + imp_stadium) <= 50  # example constraint
    problem += pollutionidx <= 500  # example constraint on pollution

    # Solve the problem
    problem.solve()

    # Collect results
    results = {
        "Coal Mine": imp_coalmine.value(),
        "Oil Well": imp_oilwell.value(),
        "Uranium Mine": imp_uramine.value(),
        "Lead Mine": imp_leadmine.value(),
        "Iron Mine": imp_ironmine.value(),
        "Bauxite Mine": imp_bauxitemine.value(),
        "Farm": imp_farm.value(),
        "Gas Refinery": imp_gasrefinery.value(),
        "Aluminum Refinery": imp_aluminumrefinery.value(),
        "Munitions Factory": imp_munitionsfactory.value(),
        "Steel Mill": imp_steelmill.value(),
        "Police Station": imp_policestation.value(),
        "Hospital": imp_hospital.value(),
        "Recycling Center": imp_recyclingcenter.value(),
        "Subway": imp_subway.value(),
        "Supermarket": imp_supermarket.value(),
        "Bank": imp_bank.value(),
        "Mall": imp_mall.value(),
        "Stadium": imp_stadium.value(),
        "Revenue": revenue,
        "Pollution": pollutionidx,
        "Disease": disease
    }

    return results

# Streamlit app

st.markdown("## City Build Optimizer")

with st.form("city_build_form"):
    infra = st.number_input("Infrastructure Level", min_value=0, step=1)
    land = st.number_input("Land", min_value=0, step=1)
    armstockpile = st.checkbox("Arms Stockpile")
    bauxiteworks = st.checkbox("Bauxite Works")
    emergencygas = st.checkbox("Emergency Gas Reserve")
    ironworks = st.checkbox("Iron Works")
    uraniumenrich = st.checkbox("Uranium Enrichment")
    clinicalresearch = st.checkbox("Clinical Research Center")
    greentech = st.checkbox("Green Technology")
    governmentsupport = st.checkbox("Government Support Agency")
    itc = st.checkbox("International Trade Center")
    massirrigation = st.checkbox("Mass Irrigation Program")
    recycling = st.checkbox("Recycling Initiative")
    policeprogram = st.checkbox("Police Program Initiative")
    telesat = st.checkbox("Telecommunications Satellite")
    openmarkets = st.checkbox("Open Markets")

    submitted = st.form_submit_button("Optimize")

if submitted:
    results = optimize_city_build(infra, land, armstockpile, bauxiteworks, emergencygas, ironworks, uraniumenrich, clinicalresearch, greentech, governmentsupport, itc, massirrigation, recycling, policeprogram, telesat, openmarkets)

if results:
    st.success("Optimization Complete!")
    st.json(results)

fig = px.bar(pd.DataFrame(results.items(), columns=["Structure", "Value"]), x="Structure", y="Value")
st.plotly_chart(fig)

