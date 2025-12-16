import streamlit as st
from typing import Dict, Any

from utils import (
    create_sliders_from_csv,
    load_data,
    beautifulize,
    get_thb_exchange_rate
)
from computation import (
    compute_mother_impact_cohort,
    compute_women_moderately_depressed,
    calculate_severe_depression,
    calculate_women_with_anxiety,
    calculate_mother_suicide,
    calculate_dalys_and_dalyusd,
    calculate_income_loss_depression,
    calculate_income_loss_anxiety,
    calculate_exposed_children,
    calculate_dalys_children,
    calculate_income_loss_children,
    calculate_healthcare_costs_first_year,
    calculate_totals
)
from visualizations import (
    display_cost_overview,
    render_cost_types_piechart,
    render_costs_barchart_2,
)

st.set_page_config(
    page_title="PMH Web Tool",
    page_icon="icon2.png",
    layout="wide", 
    initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        max-width: 600px;
        min-width: 600px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data #Prevents this function from executing unless the inputs change (othewise would rerun on every user interaction)
def perform_computations(
    parameters: Dict[str, Any], currency_symbol: str, currency_code: str, conversion_rate: float) -> Dict[str, Any]:
    computations = [
        ("result_mother_cohort", compute_mother_impact_cohort), #Number of women in the cohort at different timepoints
        ("result_depression", compute_women_moderately_depressed), #Number of moderately depressed women in the cohort at different timepoints
        ("result_depression_severe", calculate_severe_depression), #Number of severely depressed women in the cohort at different timepoints
        ("result_anxiety", calculate_women_with_anxiety), #Number of women with anxiety in the cohort at different timepoints
        ("result_suicide", calculate_mother_suicide), #Number of women committing suicide
        ("result_dalys", calculate_dalys_and_dalyusd), #Disability-Adjusted Life Years (lost?) from all above women and timepoints
        ("result_loss_depression", calculate_income_loss_depression), #Income loss from depression at different timepoints
        ("result_loss_anxiety", calculate_income_loss_anxiety), #Income loss from anxiety at different timepoints
        ("result_exposed_children", calculate_exposed_children), #Numbers of additional children with outcomes due to exposure
        ("result_dalys_children", calculate_dalys_children),
        ("result_income_loss_children", calculate_income_loss_children),
        ("result_healthcare_costs_first_year", calculate_healthcare_costs_first_year),
        ("results_totals", calculate_totals)
    ]

    for result_name, computation_function in computations:
        result = computation_function(parameters)
        parameters.update(result) #The key-value pairs for the results are added to the dict of the input parameters

    parameters["currency_symbol"] = currency_symbol
    parameters["currency_code"] = currency_code
    parameters["conversion_rate"] = conversion_rate

    return parameters




#st.sidebar.text(" - Add description here of how to adjust input parameters - ")
#st.sidebar.text(" - Use checkboxes to toggle number input - ")



st.sidebar.markdown("""
<style>
.sidebar-header {
    font-size: 42px !important;
    
    margin-bottom: 20px;
}
</style>
<div class="sidebar-header">Data Inputs</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    'A guide on how to collect the data required for this tool can be found <a href="https://docs.google.com/document/d/184xA7ncuAgh5N30G4XXRu11rXGMPkwMi/edit" target="_blank">here</a>.', 
    unsafe_allow_html=True
)

# Country input box
country_name = st.sidebar.text_input(
    "Country name to display:",
    value="Thailand"
)

st.title(f"The costs of perinatal mental health problems in {country_name}")


display_currency_settings = st.sidebar.toggle("Change currency", value=False)

if display_currency_settings:
    with st.sidebar.expander("**Currency Conversion Settings**", expanded = True):
        # currency_symbol = st.text_input("Currency symbol", value= "$")
        conversion_rate = st.number_input("Conversion rate for calculations (USD 1.0 = )", min_value=0.0, value= 1.0, step=0.001)
        currency_code = st.text_input("Currency code to display", value= "USD")
        currency_symbol = currency_code
        convert_input = True #st.toggle("Convert data input currency")
else:
    # Default values when toggle is off
    # currency_symbol = "$"
    currency_code = "USD"
    currency_symbol = currency_code
    conversion_rate = 1.0
    convert_input = True

df = load_data()
parameters = create_sliders_from_csv(df, currency_symbol, convert_input, conversion_rate)
parameters = perform_computations(parameters, currency_symbol, currency_code, conversion_rate)


if parameters:

    st.write("")

    display_cost_overview(parameters)
    with st.container():
        render_cost_types_piechart(parameters)

        #render_cost_types_piechart_2(parameters)

        #render_costs_barchart_2(parameters)
        render_costs_barchart_2(parameters)
        #render_costs_barchart_2_inside_left(parameters)


    
    

