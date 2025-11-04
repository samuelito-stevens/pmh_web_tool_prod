import streamlit as st
import pandas as pd
import requests

ADMIN_PASSWORD = "vertigo"

@st.cache_data(ttl=3600)
def get_thb_exchange_rate():
    try:
        response = requests.get("https://api.exchangeratesapi.io/v1/latest?access_key=YOUR_API_KEY&base=USD&symbols=THB")
        data = response.json()
        return data["rates"]["THB"]
    except:
        return 32.4 #default fallback exchange rate



def beautifulize(dict_result, name):
    return pd.Series(dict_result, name=name.replace("_", " ").title()).astype(int)


@st.cache_data
def load_data():
    df = pd.read_excel(
        "Cost model data structure.xlsx", sheet_name="inputs", skiprows=1
    )

    # remove any leading spaces that would create several sections -- not sure exactly how this is working
    for col in df.select_dtypes(include=object).columns:
        df[col] = df[col].str.strip()

    return df.dropna(how="all").dropna(how="all", axis=1)


def format_large_number(number: float, currency: str = "$") -> str:
    abs_number = abs(number)

    if abs_number >= 1e9:
        formatted = f"{currency}{abs_number/1e9:.3g}B"
    elif abs_number >= 1e6:
        formatted = f"{currency}{abs_number/1e6:.3g}M"
    elif abs_number >= 1e3:
        formatted = f"{currency}{abs_number/1e3:.3g}k"
    else:
        formatted = f"{currency}{abs_number:.3g}"

    # Remove trailing zeros after the decimal point
    formatted = formatted.rstrip("0").rstrip(".") if "." in formatted else formatted

    return formatted

def format_large_number_long(number: float, currency: str = "$") -> str:
    abs_number = abs(number)

    if abs_number >= 1e12:
        formatted = f"{currency}{abs_number/1e12:.3g} Trillion"
    elif abs_number >= 1e9:
        formatted = f"{currency}{abs_number/1e9:.3g} Billion"
    elif abs_number >= 1e6:
        formatted = f"{currency}{abs_number/1e6:.3g} Million"
    elif abs_number >= 1e3:
        formatted = f"{currency}{abs_number/1e3:.3g} thousand"
    else:
        formatted = f"{currency}{abs_number:.3g}"

    # Remove trailing zeros after the decimal point
    formatted = formatted.rstrip("0").rstrip(".") if "." in formatted else formatted

    return formatted


def check_admin_access() -> bool:
    is_admin = st.sidebar.checkbox("Are you an admin?")
    if is_admin:
        password = st.sidebar.text_input("Enter admin password:", type="password")
        if password == ADMIN_PASSWORD:
            st.sidebar.success("Admin mode activated!")
            return True
        elif password:
            st.sidebar.error("Incorrect password. Please try again.")
    return False


def create_sliders_from_csv(df, currency_code, convert_input, conversion_rate):
    """
    Create Streamlit sliders from a CSV DataFrame with parameters.
    
    Expected DataFrame columns:
    - Section: Main grouping category
    - Subsection: Sub-grouping within section
    - Variable name: Display name for the slider
    - Default Value: Initial slider value
    - Is Tunable By User?: Whether slider should be enabled ('Yes'/'No')
    - Min range
    - Max range
    - Unit: Unit type (e.g., 'percentage', 'count', etc.)
    - Tooltip
    
    Returns:
    - dict: Parameter values keyed by "{Section}_{Subsection}_{Variable name}"
    """

    params = {}
    
    # Validate required columns
    required_columns = ['Section', 'Subsection', 'Variable name', 'Default Value', 'Is Tunable By User?', 'Min range', 'Max range', 'Unit', 'Tooltip']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        return params
    
    # Handle potential NaN values
    df = df.fillna('')
    
    grouped = df.groupby("Section", sort=False)
    
    for section, group in grouped:
        if (section != "Mothers + children impact"): # Mothers + Children impact section has no tunable parameters
            st.sidebar.markdown(f"## {section}")
        
        subgrouped = group.groupby("Subsection", sort=False)
        
        for subsection, subgroup in subgrouped:

            has_tunable_variables = False
            tunable_rows = []
            
            for _, row in subgroup.iterrows():
                # Create unique key
                key = f"{row['Section']}_{row['Subsection']}_{row['Variable name']}"
                # Parse and validate default value
                try:
                    default_value = float(row["Default Value"])
                except (ValueError, TypeError):
                    st.warning(f"Invalid default value for {row['Variable name']}: {row['Default Value']}")
                    continue
                # Determine if slider should be disabled
                is_disabled = str(row["Is Tunable By User?"]).strip().lower() != "yes"

                if is_disabled:
                    # Store non-tunable parameters directly
                    params[key] = default_value
                else:
                    # This subgroup has at least one tunable variable
                    has_tunable_variables = True
                    tunable_rows.append(row)

            #Only create expander if there are tunable variables
            if has_tunable_variables:
                clean_subsection = subsection.replace(", in USD", "") if subsection else ""
                expander_label = clean_subsection if clean_subsection.strip() else "General"

                with st.sidebar.expander(expander_label, expanded=False):
                    for row in tunable_rows:
                        try:
                            # Create unique key
                            key = f"{row['Section']}_{row['Subsection']}_{row['Variable name']}"

                            try:
                                default_value = float(row["Default Value"])
                            except (ValueError, TypeError):
                                continue

                            try:
                                max_value = float(row["Max range"])
                                min_value = float(row["Min range"])
                            except (ValueError, TypeError):
                                st.warning(f"Invalid min or max value for {row['Variable name']}")
                                continue

                            # Check if it's a percentage
                            is_percentage = str(row["Unit"]).lower().strip() == "percentage"

                            # Determine appropriate step size
                            if is_percentage:
                                step = 0.1  # 0.1% steps for percentages
                            elif abs(max_value) < 0.01:
                                step = 0.00001  # Smaller steps for small values
                            elif abs(max_value) < 0.1:
                                step = 0.0001 
                            elif abs(max_value) < 1:
                                step = 0.001 
                            elif abs(max_value) < 10:
                                step = 0.01
                            elif abs(max_value) > 100:
                                step = 1
                            else:
                                step = 0.1

                            # Create informative tooltip
                            #tooltip = f"{row["Tooltip"]}"
                            #tooltip = (f"Unit: {row['Unit']}\n"
                            #         f"Default: {row['Default Value']}\n"
                            #         f"Range: {min_value:.2f} to {max_value:.2f}")

                            # Adjust display value for percentages
                            display_default = default_value * 100 if is_percentage else default_value
                            display_max = max_value
                            display_min = min_value

                            use_text_input = str(row['Text input']).strip().lower() == "yes" 
                            use_currency_formatting = str(row["Unit"]).strip().lower() == "currency"

                                # Create the input control based on mode
                            slider_label = f"{row['Display name']}"
                            
                            #with col1:
                            if use_currency_formatting:
                                col1, col2 = st.columns([0.06, 0.94])
                                with col1:
                                    st.markdown(f"<div style='padding-top: 35.5px; padding-left: 0px; font-size: 16px;'>{currency_code if convert_input else "USD"}</div>", unsafe_allow_html=True)
                                with col2:
                                    display_value = st.number_input(
                                        slider_label,
                                        min_value=float(display_min * conversion_rate if convert_input else display_min),
                                        max_value=float(display_max * conversion_rate if convert_input else display_max),
                                        value=float(display_default * conversion_rate if convert_input else display_default),
                                        step=float(step),
                                        key=f"{key}_number",
                                        #disabled=is_disabled,
                                        #help=tooltip,
                                        format="%.0f"
                                    )
                            elif use_text_input:
                                # Use number input for precise values
                                display_value = st.number_input(
                                    slider_label,
                                    min_value=float(display_min),
                                    max_value=float(display_max),
                                    value=float(display_default),
                                    step=float(step),
                                    key=f"{key}_number",
                                    #disabled=is_disabled,
                                    #help=tooltip,
                                    format="%g"
                                )
                            else:

                                # Use slider for visual adjustment
                                display_value = st.slider(
                                    slider_label,
                                    min_value=float(display_min),
                                    max_value=float(display_max),
                                    value=float(display_default),
                                    step=float(step),
                                    key=f"{key}_slider",
                                    format="%g%%" if is_percentage else "%g",
                                )

                            # Store the actual value (convert back from percentage if needed)
                            if is_percentage:
                                actual_value = display_value / 100
                            elif use_currency_formatting:
                                actual_value = display_value / conversion_rate if convert_input else display_value
                            else:
                                actual_value = display_value
                            params[key] = actual_value

                        except Exception as e:
                            st.error(f"Error creating slider for {row.get('Variable name', 'Unknown')}: {str(e)}")
                            continue

        # Add visual separator between sections
        #st.sidebar.markdown("---")
    
    return params
