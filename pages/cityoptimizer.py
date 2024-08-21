import streamlit as st
import pandas as pd
import plotly.express as px
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpInteger

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

    def calculate_production(variable, base_production, scaling_factor):
        variable_value = variable.varValue if variable.varValue is not None else 0
        return base_production * (1 + (scaling_factor / 9) * (variable_value - 1))


    bauxiteproduced = calculate_production(imp_bauxitemine, 3, 0.5)
    coalproduced = calculate_production(imp_coalmine, 3, 0.5)
    ironproduced = calculate_production(imp_ironmine, 3, 0.5)
    leadproduced = calculate_production(imp_leadmine, 3, 0.5)
    oilproduced = calculate_production(imp_oilwell, 3, 0.5)
    uraniumproduced = calculate_production(imp_uramine, 3, 0.5) * (2 if uraniumenrich else 1)
    foodproduced = (imp_farm.varValue * (land / (400 if massirrigation else 500))) * 12
    steelmultiplier = 12.24 if ironworks else 9
    steelproduced = calculate_production(imp_steelmill, steelmultiplier, 0.125)
    gasmultiplier = 12 if emergencygas else 9
    gasproduced = calculate_production(imp_gasrefinery, gasmultiplier, 0.125)
    aluminummultiplier = 12.24 if bauxiteworks else 9
    aluminumproduced = round(calculate_production(imp_aluminumrefinery, aluminummultiplier, 0.125), 2)
    munitionsmultiplier = 24.12 if armstockpile else 18
    munitionsproduced = calculate_production(imp_munitionsfactory, munitionsmultiplier, 0.125)

    # Calculate Pollution Index
    pollutionidx = (
        imp_coalmine.varValue * 12 + imp_oilwell.varValue * 12 + imp_bauxitemine.varValue * 12 +
        imp_leadmine.varValue * 12 + imp_ironmine.varValue * 12 + imp_uramine.varValue * 20 +
        (imp_farm.varValue * (1 if greentech else 2)) + (imp_gasrefinery.varValue * (24 if greentech else 32)) +
        (imp_aluminumrefinery.varValue * (30 if greentech else 40)) + (imp_steelmill.varValue * (30 if greentech else 40)) +
        (imp_munitionsfactory.varValue * (24 if greentech else 32)) + imp_policestation.varValue * 1 +
        imp_hospital.varValue * 4 + (imp_recyclingcenter.varValue * (-75 if recycling else -70)) +
        (imp_subway.varValue * (-70 if greentech else -45)) + imp_mall.varValue * 2 + imp_stadium.varValue * 5
    )
    pollutionidx = max(pollutionidx, 0)

    # Calculate Disease
    basepopulation = infra * 100
    popdensity = basepopulation / land
    diseasemultiplier = 3.5 if clinicalresearch else 2.5
    disease = round(
        ((((popdensity**2) * 0.01) - 25) / 100) + (basepopulation / 100000) + (pollutionidx * 0.05) - 
        imp_hospital.varValue * diseasemultiplier, 2
    )

    # Calculate Commerce Revenue
    if telesat and not itc:
        st.error("You must have International Trade Center and Telecommunications Satellite to use Telecommunications Satellite")
        return None
    total_commerce = imp_supermarket.varValue * 3 + imp_bank.varValue * 5 + imp_mall.varValue * 9 + imp_stadium.varValue * 12 + imp_subway.varValue * 8
    commerce_bonus = 2 if telesat and itc else 0
    
    commercerev = round((((min(total_commerce + commerce_bonus, 125) / 50) * 0.725) + 0.725) * basepopulation, 2)
    commercerev = commercerev * 1.015 if openmarkets and governmentsupport else commercerev * 1.01 if openmarkets else commercerev

    # Calculate Revenue
    rssrevenue = (
        (foodproduced * 5) +
        (coalproduced * 5) +
        (oilproduced * 5) +
        (ironproduced * 5) +
        (uraniumproduced * 5) +
        (bauxiteproduced * 5) +
        (leadproduced * 5) +
        (gasproduced * 5) +
        (munitionsproduced * 5) +
        (aluminumproduced * 5) +
        (steelproduced * 5)
    )

    # Objective function
    problem += rssrevenue + commercerev, "TotalRevenue"

    # Constraints
    problem += (imp_coalmine + imp_oilwell + imp_uramine + imp_leadmine + imp_ironmine + imp_bauxitemine +
                imp_farm + imp_gasrefinery + imp_aluminumrefinery + imp_munitionsfactory + imp_steelmill +
                imp_policestation + imp_hospital + imp_recyclingcenter + imp_subway + imp_supermarket +
                imp_bank + imp_mall + imp_stadium) <= 50  # example constraint
    problem += pollutionidx <= 500  # example constraint on pollution

    # Solve the problem
    problem.solve()

    # Extract results
    results = {
        "CoalMine": imp_coalmine.varValue,
        "OilWell": imp_oilwell.varValue,
        "UraniumMine": imp_uramine.varValue,
        "LeadMine": imp_leadmine.varValue,
        "IronMine": imp_ironmine.varValue,
        "BauxiteMine": imp_bauxitemine.varValue,
        "Farm": imp_farm.varValue,
        "GasRefinery": imp_gasrefinery.varValue,
        "AluminumRefinery": imp_aluminumrefinery.varValue,
        "MunitionsFactory": imp_munitionsfactory.varValue,
        "SteelMill": imp_steelmill.varValue,
        "PoliceStation": imp_policestation.varValue,
        "Hospital": imp_hospital.varValue,
        "RecyclingCenter": imp_recyclingcenter.varValue,
        "Subway": imp_subway.varValue,
        "Supermarket": imp_supermarket.varValue,
        "Bank": imp_bank.varValue,
        "Mall": imp_mall.varValue,
        "Stadium": imp_stadium.varValue,
        "TotalRevenue": lpSum([rssrevenue, commercerev]).value()
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