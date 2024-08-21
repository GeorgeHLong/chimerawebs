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
    massirrigation = LpVariable("MassIrrigationProgram", cat=LpBinary)
    recycling = LpVariable("RecyclingProgram", cat=LpBinary)
    policeprogram = LpVariable("PoliceProgram", cat=LpBinary)
    telesat = LpVariable("TelecommunicationsSatellite", cat=LpBinary)
    openmarkets = LpVariable("OpenMarkets", cat=LpBinary)

    # Helper variables for production calculations
    bauxiteproduced = LpVariable("BauxiteProduced", lowBound=0)
    coalproduced = LpVariable("CoalProduced", lowBound=0)
    ironproduced = LpVariable("IronProduced", lowBound=0)
    leadproduced = LpVariable("LeadProduced", lowBound=0)
    oilproduced = LpVariable("OilProduced", lowBound=0)
    uraniumproduced = LpVariable("UraniumProduced", lowBound=0)
    foodproduced = LpVariable("FoodProduced", lowBound=0)
    steelproduced = LpVariable("SteelProduced", lowBound=0)
    gasproduced = LpVariable("GasProduced", lowBound=0)
    aluminumproduced = LpVariable("AluminumProduced", lowBound=0)
    munitionsproduced = LpVariable("MunitionsProduced", lowBound=0)

    # Constraints for production calculations
    problem += bauxiteproduced == ((imp_bauxitemine * 3) * (1 + (0.5 / 9) * (imp_bauxitemine - 1)))
    problem += coalproduced == ((imp_coalmine * 3) * (1 + (0.5 / 9) * (imp_coalmine - 1)))
    problem += ironproduced == ((imp_ironmine * 3) * (1 + (0.5 / 9) * (imp_ironmine - 1)))
    problem += leadproduced == ((imp_leadmine * 3) * (1 + (0.5 / 9) * (imp_leadmine - 1)))
    problem += oilproduced == ((imp_oilwell * 3) * (1 + (0.5 / 9) * (imp_oilwell - 1)))
    problem += uraniumproduced == (imp_uramine * 3 * (1 + (0.5 / 4) * (imp_uramine - 1))) * (2 if uraniumenrich else 1)
    problem += foodproduced == (imp_farm * (land / (400 if massirrigation else 500))) * 12

    steelmultiplier = 12.24 if ironworks else 9
    problem += steelproduced == (imp_steelmill * steelmultiplier) * (1 + 0.125 * (imp_steelmill - 1))

    gasmultiplier = 12 if emergencygas else 9
    problem += gasproduced == (imp_gasrefinery * gasmultiplier) * (1 + 0.125 * (imp_gasrefinery - 1))

    aluminummultiplier = 12.24 if bauxiteworks else 9
    problem += aluminumproduced == (imp_aluminumrefinery * aluminummultiplier) * (1 + 0.125 * (imp_aluminumrefinery - 1))

    munitionsmultiplier = 24.12 if armstockpile else 18
    problem += munitionsproduced == (imp_munitionsfactory * munitionsmultiplier) * (1 + 0.125 * (imp_munitionsfactory - 1))

    # Pollution calculation and constraint
    pollutionidx = (
        imp_coalmine * 12 + imp_oilwell * 12 + imp_bauxitemine * 12 + imp_leadmine * 12 + imp_ironmine * 12 +
        imp_uramine * 20 + (imp_farm * (1 + (0.25 if massirrigation else 0.5))) +
        imp_gasrefinery * 24 + imp_aluminumrefinery * 12 + imp_munitionsfactory * 12 + imp_steelmill * 24 +
        imp_policestation * (-6) + imp_hospital * (-12) + imp_recyclingcenter * (-12) + imp_subway * (-12)
    )
    # Disease calculation
    disease = max(0, (0.01 * pollutionidx) + (0.005 * infra) - (0.001 * imp_hospital))

    # Resource and Commerce Revenue Calculation
    rssrevenue = (bauxiteproduced * 2400) + (coalproduced * 2400) + (ironproduced * 2400) + (leadproduced * 2400) + (oilproduced * 2400) + (uraniumproduced * 4800) + (foodproduced * 1600) + (steelproduced * 3000) + (gasproduced * 3000) + (aluminumproduced * 3000) + (munitionsproduced * 6000)
    
    commercerev = (imp_supermarket * 20000) + (imp_bank * 40000) + (imp_mall * 40000) + (imp_stadium * 80000)
    
    revenue = round(rssrevenue + commercerev, 2)
    
    # Objective: Maximize revenue
    problem += revenue

    # Constraints
    problem += (imp_coalmine + imp_oilwell + imp_uramine + imp_leadmine + imp_ironmine + imp_bauxitemine + imp_farm + imp_gasrefinery + imp_aluminumrefinery + imp_munitionsfactory + imp_steelmill + imp_policestation + imp_hospital + imp_recyclingcenter + imp_subway + imp_supermarket + imp_bank + imp_mall + imp_stadium) <= 50  # Example constraint
    problem += pollutionidx <= 500  # Example constraint on pollution

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