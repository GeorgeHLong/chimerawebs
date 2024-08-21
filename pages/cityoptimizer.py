import streamlit as st
import json
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

    # Calculations
    # Production calculations for resources
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
        imp_coalmine * 12 + imp_oilwell * 12 + imp_bauxitemine * 12 + imp_leadmine * 12 + imp_ironmine * 12 + 
        imp_uramine * 20 + (imp_farm * (1 if greentech else 2)) + 
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

    # Revenue calculation
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

    # Objective function
    problem += commercerev + rssrevenue, "TotalRevenue"

    # Solve the problem
    problem.solve()

    # Extract results
    result = {
        'Coal Mines': imp_coalmine.varValue,
        'Oil Wells': imp_oilwell.varValue,
        'Uranium Mines': imp_uramine.varValue,
        'Lead Mines': imp_leadmine.varValue,
        'Iron Mines': imp_ironmine.varValue,
        'Bauxite Mines': imp_bauxitemine.varValue,
        'Farms': imp_farm.varValue,
        'Gas Refineries': imp_gasrefinery.varValue,
        'Aluminum Refineries': imp_aluminumrefinery.varValue,
        'Munitions Factories': imp_munitionsfactory.varValue,
        'Steel Mills': imp_steelmill.varValue,
        'Police Stations': imp_policestation.varValue,
        'Hospitals': imp_hospital.varValue,
        'Recycling Centers': imp_recyclingcenter.varValue,
        'Subways': imp_subway.varValue,
        'Supermarkets': imp_supermarket.varValue,
        'Banks': imp_bank.varValue,
        'Malls': imp_mall.varValue,
        'Stadiums': imp_stadium.varValue
    }

    return result

# Example usage
infra = 1000
land = 500
armstockpile = True
bauxiteworks = False
emergencygas = True
ironworks = False
uraniumenrich = True
clinicalresearch = False
greentech = True
governmentsupport = False
itc = True
massirrigation = False
recycling = True
policeprogram = False
telesat = True
openmarkets = False

optimal_build = optimize_city_build(infra, land, armstockpile, bauxiteworks, emergencygas, ironworks, uraniumenrich, clinicalresearch, greentech, governmentsupport, itc, massirrigation, recycling, policeprogram, telesat, openmarkets)
st.write("Optimal City Build:", optimal_build)
