import pandas as pd

################################################### MOTHER IMPACT ##############################################################

def compute_mother_impact_cohort(parameters):
    live_births = parameters["Mothers' impact_Cohort_Live births"]
    mortality_probability_women_15_39 = parameters[
        "Mothers' impact_Cohort_Mortality probability (women aged 15 to 39yrs)"
    ]

    number_women_antenatal_period = live_births / (#Edited formula compared to original spreadsheet
        1
        - parameters["Mothers' impact_Cohort_Still birth rate (per 1,000)"] / 1000
    ) 

    number_women_postnatal_period = live_births * (#Should work, but why does this not include still births and the other does?
        1
        - parameters["Mothers' impact_Cohort_Mortality probability during / after birth"]
    )

    results = {
        "Number of women antenatal period": number_women_antenatal_period,
        "Number of women postnatal period": number_women_postnatal_period,
    }

    results["Number of women Year + 1"] = number_women_postnatal_period * (
        1 - mortality_probability_women_15_39
    )

    for year in range(2, 11):
        results[f"Number of women Year + {year}"] = results[
            f"Number of women Year + {year - 1}"
        ] * (1 - mortality_probability_women_15_39)

    return results


def compute_women_moderately_depressed(parameters):
    results = {}

    postnatal_depression_prevalence = parameters[
        "Mothers' impact_With postnatal mental health problems_Prevalence postnatal depression (moderate or severe)"
    ]
    postnatal_moderate_proportion = parameters[
        "Mothers' impact_With postnatal mental health problems_Proportion of postnatal depression that is moderate depression"
    ]

    results["Number women moderately depressed antenatal"] = (
        parameters["Number of women antenatal period"]
        * parameters[
            "Mothers' impact_With antenatal mental health problems_Prevalence / probability antenatal depression (moderate and severe only)"
        ]
        * parameters[
            "Mothers' impact_With antenatal mental health problems_Proportion of antenatal depression that is moderate depression"
        ]
    )
    results["Number women moderately depressed postnatal"] = (
        parameters["Number of women postnatal period"]
        * postnatal_depression_prevalence
        * postnatal_moderate_proportion
    )

    for year in range(1, 11):
        results[f"Number women moderately depressed Year + {year}"] = (
            parameters[f"Number of women Year + {year}"]
            * postnatal_depression_prevalence
            * postnatal_moderate_proportion
            * parameters[
                "Mothers' impact_With ongoing mental health problems_Prevalence / probability ongoing depression" #Is the math right here?
            ]
        )

    return results


def calculate_severe_depression(parameters):
    results = {}

    results["Number women severely depressed antenatal"] = (
        parameters["Number of women antenatal period"]
        * parameters[
            "Mothers' impact_With antenatal mental health problems_Prevalence / probability antenatal depression (moderate and severe only)"
        ]
        * parameters[
            "Mothers' impact_With antenatal mental health problems_Proportion of antenatal depression that is severe depression"
        ]
    )
    results["Number women severely depressed postnatal"] = (
        parameters["Number of women postnatal period"]
        * parameters[
            "Mothers' impact_With postnatal mental health problems_Prevalence postnatal depression (moderate or severe)"
        ]
        * parameters[
            "Mothers' impact_With postnatal mental health problems_Proportion of postnatal depression that is severe depression"
        ]
    )

    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results[f"Number women severely depressed {year}"] = (
            parameters[f"Number of women {year}"]
            * parameters[
                "Mothers' impact_With postnatal mental health problems_Prevalence postnatal depression (moderate or severe)"
            ]
            * parameters[
                "Mothers' impact_With postnatal mental health problems_Proportion of postnatal depression that is severe depression"
            ]
            * parameters[
                "Mothers' impact_With ongoing mental health problems_Prevalence / probability ongoing depression"
            ]
        )

    return results


def calculate_women_with_anxiety(parameters):
    results = {}

    results["Number women anxious antenatal"] = (
        parameters["Number of women antenatal period"]
        * parameters[
            "Mothers' impact_With antenatal mental health problems_Prevalence / probability antenatal anxiety (any) without depression"
        ]
    )

    results["Number women anxious postnatal"] = (
        parameters["Number of women postnatal period"]
        * parameters[
            "Mothers' impact_With postnatal mental health problems_Prevalence / probability postnatal anxiety (any) without depression"
        ]
    )

    for i in range(1, 11):
        year = f"Year + {i}"
        results[f"Number women anxious {year}"] = (
            parameters[f"Number of women {year}"]
            * parameters[
                "Mothers' impact_With postnatal mental health problems_Prevalence / probability postnatal anxiety (any) without depression"
            ]
            * parameters[
                "Mothers' impact_With ongoing mental health problems_Prevalence / probability ongoing anxiety"
            ]
        )

    return results


def calculate_mother_suicide(parameters):
    results = {
        "Number women committing suicide ante- and postnatal": int(
            parameters[
                "Mothers' impact_Years of Life Lost_Suicide rate ante- and postnatal period (per 100,000)"
            ]
            * (
                (
                    parameters["Number of women antenatal period"]
                    + parameters["Number of women postnatal period"]
                )
                / 100000 
            )
        )
    }

    return results


def calculate_dalys_and_dalyusd(parameters):
    results = {}

    results["DALYs women moderately depressed antenatal"] = (
        parameters["Number women moderately depressed antenatal"]
        * parameters["Mothers' impact_With ongoing mental health problems_Duration of perinatal mental health problems"]
        * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for moderate depression"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 0)

    results["DALYs women moderately depressed postnatal"] = (
        parameters["Number women moderately depressed postnatal"]
        * parameters["Mothers' impact_With ongoing mental health problems_Duration of perinatal mental health problems"]
        * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for moderate depression"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 1)

    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results[f"DALYs women moderately depressed {year}"] = (
            parameters[f"Number women moderately depressed {year}"]
            * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for moderate depression"]
        ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** (year_int + 1))

    results["DALYs women severely depressed antenatal"] = (
        parameters["Number women severely depressed antenatal"]
        * parameters["Mothers' impact_With ongoing mental health problems_Duration of perinatal mental health problems"]
        * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for severe depression"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 0)

    results["DALYs women severely depressed postnatal"] = (
        parameters["Number women severely depressed postnatal"]
        * parameters["Mothers' impact_With ongoing mental health problems_Duration of perinatal mental health problems"]
        * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for severe depression"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 1)

    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results[f"DALYs women severely depressed {year}"] = (
            parameters[f"Number women severely depressed {year}"]
            * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for severe depression"]
        ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** (year_int + 1))

    results["DALYs women anxious antenatal"] = (
        parameters["Number women anxious antenatal"]
        * parameters["Mothers' impact_With ongoing mental health problems_Duration of perinatal mental health problems"]
        * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for moderate anxiety"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 0)

    results["DALYs women anxious postnatal"] = (
        parameters["Number women anxious postnatal"]
        * parameters["Mothers' impact_With ongoing mental health problems_Duration of perinatal mental health problems"]
        * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for moderate anxiety"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 1)

    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results[f"DALYs women anxious {year}"] = (
            parameters[f"Number women anxious {year}"]
            * parameters["Mothers' impact_Disability Adjusted Life Years_Disability weight for moderate anxiety"]
        ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** (year_int + 1))

    # Suicide
    results["DALYs women committing suicide ante and postnatal"] = (
        parameters["Number women committing suicide ante- and postnatal"]
        * parameters["Mothers' impact_Years of Life Lost_Years of Life Lost due to suicide"])


    # Total DALYS for moderate depression
    results["DALYs women moderately depressed"] = (
        results["DALYs women moderately depressed antenatal"]
        + results["DALYs women moderately depressed postnatal"]
    )
    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results["DALYs women moderately depressed"] += results[f"DALYs women moderately depressed {year}"]

    # Total DALYs for severe depression
    results["DALYs women severely depressed"] = (
        results["DALYs women severely depressed antenatal"]
        + results["DALYs women severely depressed postnatal"]
    )
    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results["DALYs women severely depressed"] += results[f"DALYs women severely depressed {year}"]
    
    # Total DALYs for anxiety
    results["DALYs women anxious"] = (
        results["DALYs women anxious antenatal"]
        + results["DALYs women anxious postnatal"]
    )
    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results["DALYs women anxious"] += results[f"DALYs women anxious {year}"]

    # DALYs in USD
    gdp_per_capita = parameters["Mothers' impact_Valuing quality of life loss, in USD_GDP per capita"]
    daly_weight = parameters["Mothers + children impact_Valuing quality of life loss, in USD_Weight for valuing DALY with GDP per capita"]
    
    base_results = results.copy()
    for key, value in base_results.items():
        results[f"{key}, in USD"] = value * gdp_per_capita * daly_weight

    return results


def calculate_income_loss_depression(parameters):
    results = {}

    results["Income loss women depression antenatal"] = (
        (parameters["Number women moderately depressed antenatal"]
            + parameters["Number women severely depressed antenatal"]
        ) * parameters["Mothers' impact_Valuing productivity loss, in USD_Income decrement depression women per year, in USD"]
    )

    results["Income loss women depression postnatal"] = (
        (parameters["Number women moderately depressed postnatal"]
            + parameters["Number women severely depressed postnatal"]
        ) * parameters["Mothers' impact_Valuing productivity loss, in USD_Income decrement depression women per year, in USD"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 1)

    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results[f"Income loss women depression {year}"] = (
            (parameters[f"Number women moderately depressed {year}"]
                + parameters[f"Number women severely depressed {year}"]
            ) * parameters["Mothers' impact_Valuing productivity loss, in USD_Income decrement depression women per year, in USD"]
        ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** (year_int + 1))

    # Total income loss due to depression:
    results["Income loss women depression"] = (
        results["Income loss women depression antenatal"]
        + results["Income loss women depression postnatal"]
    )
    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results["Income loss women depression"] += results[f"Income loss women depression {year}"]

    return results


def calculate_income_loss_anxiety(parameters):
    results = {}

    results["Income loss women anxiety antenatal"] = (
        parameters["Number women anxious antenatal"]
        * parameters["Mothers' impact_Valuing productivity loss, in USD_Income decrement anxiety women per year, in USD"]
    )

    results["Income loss women anxiety postnatal"] = (
        parameters["Number women anxious postnatal"]
        * parameters["Mothers' impact_Valuing productivity loss, in USD_Income decrement anxiety women per year, in USD"]
    ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** 1)

    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results[f"Income loss women anxiety {year}"] = (
            parameters[f"Number women anxious {year}"]
            * parameters["Mothers' impact_Valuing productivity loss, in USD_Income decrement anxiety women per year, in USD"]
        ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"]** (year_int + 1))

    # Total income loss due to anxiety:
    results["Income loss women anxiety"] = (
        results["Income loss women anxiety antenatal"]
        + results["Income loss women anxiety postnatal"]
    )
    for year_int in range(1, 11):
        year = f"Year + {year_int}"
        results["Income loss women anxiety"] += results[f"Income loss women anxiety {year}"]

    return results

#################################################### Children's impact ###############################################################

# Number of children with problems due to exposure
def calculate_exposed_children(parameters):
    results = {}

    # Children 0 to 1 with problems due to exposure
    # Outcome 1
    results["Number of additional children outcome 1 Age 0 - 1"] = (
        parameters["Number of women antenatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 1 PRTB"]
        * parameters["Children's impact_Prevalence age 0-1_Outcome 1 pre-term birth"]
        * parameters["Children's impact_Relative risk_Outcome 1 pre-term birth"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality birth year"])

    # Outcome 2
    results["Number of additional children outcome 2 Age 0 - 1"] = (
        parameters["Number of women antenatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 2 LBW"]
        * parameters["Children's impact_Prevalence age 0-1_Outcome 2 low birth weight"]
        * parameters["Children's impact_Relative risk_Outcome 2 low birth weight"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality birth year"])

    # Outcome 3
    results["Number of additional children outcome 3 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 3 HOSP"]
        * parameters["Children's impact_Prevalence age 0-1_Outcome 3 hospitalisation"]
        * parameters["Children's impact_Relative risk_Outcome 3 hospitalisation"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"])

    # Outcome 4
    results["Number of additional children outcome 4 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 4 DIARRH"]
        * parameters["Children's impact_Prevalence age 0-1_Outcome 4 diarrhoea"]
        * parameters["Children's impact_Relative risk_Outcome 4 diarrhoea"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"])

    # Outcome 5
    results["Number of additional children outcome 5 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 5 ASTH"]
        * parameters["Children's impact_Prevalence age 0-1_Outcome 5 asthma/ severe recurring wheezing"]
        * parameters["Children's impact_Relative risk_Outcome 5 asthma/ severe recurring wheezing"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"])

    # Outcome 6
    results["Number of additional children outcome 6 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 6 LRTI"]
        * parameters["Children's impact_Prevalence age 0-1_Outcome 6 lower respiratory tract infections"]
        * parameters["Children's impact_Relative risk_Outcome 6 lower respiratory tract infections"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]) 

    # Outcome 7
    results["Number of additional children outcome 7 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 7 STUNT"]
        * parameters["Children's impact_Prevalence age 1+_Outcome 7 stunting"]
        * parameters["Children's impact_Relative risk_Outcome 7 stunting"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]) 

    # Outcome 8
    results["Number of additional children outcome 8 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 8 WAST"]
        * parameters["Children's impact_Prevalence age 1+_Outcome 8 wasting"]
        * parameters["Children's impact_Relative risk_Outcome 8 wasting"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]) 

    # Outcome 9
    results["Number of additional children outcome 9 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 9 CD"]
        * parameters["Children's impact_Prevalence age 1+_Outcome 9 conduct disorder"]
        * parameters["Children's impact_Relative risk_Outcome 9 conduct disorder"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]) 

    # Outcome 10
    results["Number of additional children outcome 10 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 10 AD"]
        * parameters["Children's impact_Prevalence age 1+_Outcome 10 attention disorder"]
        * parameters["Children's impact_Relative risk_Outcome 10 attention disorder"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]) 

    # Outcome 11
    results["Number of additional children outcome 11 Age 0 - 1"] = (
        parameters["Number of women postnatal period"]
        * parameters["Children's impact_Exposure_Prevalence of perinatal mental health condition impacting on child outcome 11 ED"]
        * parameters["Children's impact_Prevalence age 1+_Outcome 11 emotional disorder"]
        * parameters["Children's impact_Relative risk_Outcome 11 emotional disorder"]
    ) * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]) 

    # Children age 2 with problems due to exposure
    results["Number of additional children outcome 7 Age 2"] = (
        results["Number of additional children outcome 7 Age 0 - 1"]
        * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]))
    
    results["Number of additional children outcome 8 Age 2"] = (
        results["Number of additional children outcome 8 Age 0 - 1"]
        * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]))
    
    results["Number of additional children outcome 9 Age 2"] = (
        results["Number of additional children outcome 9 Age 0 - 1"]
        * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]))
    
    results["Number of additional children outcome 10 Age 2"] = (
        results["Number of additional children outcome 10 Age 0 - 1"]
        * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]))
    
    results["Number of additional children outcome 11 Age 2"] = (
        results["Number of additional children outcome 11 Age 0 - 1"]
        * (1 - parameters["Children's impact_Mortality_Mortality Years 1 to 5"]))
    
    # Children age 3 - 40 with problems due to exposure
    for year in range(3, 41):
        if (year <= 5):
            agegroup = "Years 1 to 5"
        elif (year <= 10):
            agegroup = "Years 6 to 10"
        elif (year <= 20):
            agegroup = "Years 11 to 20"
        elif (year <= 25):
            agegroup = "Years 21 to 25"
        elif (year <= 30):
            agegroup = "Years 26 to 30"
        elif (year <= 40):
            agegroup = "Years 31 to 40"
        else:
            print("AGE RANGE ERROR")
        for outcome in range(7, 12):
            results[f"Number of additional children outcome {outcome} Age {year}"] = (
                results[f"Number of additional children outcome {outcome} Age {year - 1}"]
                * (1 - parameters[f"Children's impact_Mortality_Mortality {agegroup}"])
            )

    return results

# DALYs and DALYs in USD
def calculate_dalys_children(parameters):
    results = {}
    
    # DALYs Discounted
    results["DALYs children outcome 2 LBW Lifetime"] = (
        parameters["Number of additional children outcome 2 Age 0 - 1"]
        * parameters["Children's impact_Disability Adjusted Life Years_DALYs lifetime total outcome 2 LBW"]
    )

    for outcome_int in range(8, 12):
        results[f"DALYs children outcome {outcome_int}"] = 0
        for year_int in range(5, 41):
            results[f"DALYs children outcome {outcome_int} Age {year_int}"] = (
                (parameters[f"Number of additional children outcome {outcome_int} Age {year_int}"]
                * parameters[f"Children's impact_Disability Adjusted Life Years_Disability weight outcome {outcome_int}"]
                ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** (year_int))
            )
            results[f"DALYs children outcome {outcome_int}"] += results[f"DALYs children outcome {outcome_int} Age {year_int}"]

    # DALYs in USD
    gdp_per_capita = parameters["Mothers' impact_Valuing quality of life loss, in USD_GDP per capita"]
    daly_weight = parameters["Mothers + children impact_Valuing quality of life loss, in USD_Weight for valuing DALY with GDP per capita"]
    
    base_results = results.copy()
    for key, value in base_results.items():
        results[f"{key}, in USD"] = value * gdp_per_capita * daly_weight

    return results

# Income loss
def calculate_income_loss_children(parameters):
    results = {}

    for outcome_int in (7, 9, 10, 11):
        results[f"Income loss children outcome {outcome_int}"] = 0
        for year_int in range(16, 41):
            if (outcome_int == 7):
                outcome_string = "outcome 7 stunting"
            else:
                outcome_string = "outcomes 9 to 11"
            
            results[f"Income loss children outcome {outcome_int} Age {year_int}"] = (
                (parameters[f"Number of additional children outcome {outcome_int} Age {year_int}"]
                * parameters[f"Children's impact_Valuing productivity loss, in USD_Income decrement {outcome_string}"]
                ) / (parameters["Mothers + children impact_Discounting_Discount rate +1"] ** (year_int))
            )
            results[f"Income loss children outcome {outcome_int}"] += results[f"Income loss children outcome {outcome_int} Age {year_int}"]

    return results

# Healthcare costs 1st year only
def calculate_healthcare_costs_first_year(parameters):
    results = {}

    for outcome_int in (1, 2, 4, 5, 6, 7, 8):
        results[f"Hospital cost outcome {outcome_int} Age 0 to 1"] = (
            parameters[f"Number of additional children outcome {outcome_int} Age 0 - 1"]
            * parameters[f"Children's impact_Valuing healthcare age 0-1, in USD_Outcome {outcome_int}"]
        )

    return results


####################################################   TOTALS   ###########################################################
def calculate_totals(parameters):
    results = {}

    # We already have totals over time:

    # "DALYs women moderately depressed, in USD"
    # "DALYs women severely depressed, in USD"
    # "DALYs women anxious, in USD"
    # "DALYs women committing suicide ante and postnatal, in USD"
    # "Income loss women depression"
    # "Income loss women anxiety"

    # "DALYs children outcome 2 LBW Lifetime, in USD"
    # "DALYs children outcome 8, in USD"
    # "DALYs children outcome 9, in USD"
    # "DALYs children outcome 10, in USD"
    # "DALYs children outcome 11, in USD"
    # "Income loss children outcome 7"
    # "Income loss children outcome 9"
    # "Income loss children outcome 10"
    # "Income loss children outcome 11"
    # "Hospital cost outcome 1 Age 0 to 1"
    # "Hospital cost outcome 2 Age 0 to 1"
    # "Hospital cost outcome 4 Age 0 to 1"
    # "Hospital cost outcome 5 Age 0 to 1"
    # "Hospital cost outcome 6 Age 0 to 1"
    # "Hospital cost outcome 7 Age 0 to 1"
    # "Hospital cost outcome 8 Age 0 to 1"


    results["DALYs women depressed, in USD"] = (
        parameters["DALYs women moderately depressed, in USD"] 
        + parameters["DALYs women severely depressed, in USD"]
        )
    
    results["DALYs women, in USD"] = (
        results["DALYs women depressed, in USD"] 
        + parameters["DALYs women anxious, in USD"] 
        + parameters["DALYs women committing suicide ante and postnatal, in USD"]
        )
    
    results["Income loss women"] = (
        parameters["Income loss women depression"]
        + parameters["Income loss women anxiety"]
    )

    results["Total cost women"] = (
        results["DALYs women, in USD"]
        + results["Income loss women"]
    )

    results["DALYs children, in USD"] = (
        parameters["DALYs children outcome 2 LBW Lifetime, in USD"]
        + parameters["DALYs children outcome 8, in USD"]
        + parameters["DALYs children outcome 9, in USD"]
        + parameters["DALYs children outcome 10, in USD"]
        + parameters["DALYs children outcome 11, in USD"]
    )

    results["Income loss children"] = (
        parameters["Income loss children outcome 7"]
        + parameters["Income loss children outcome 9"]
        + parameters["Income loss children outcome 10"]
        + parameters["Income loss children outcome 11"]
    )

    results["Hospital cost children"] = (
        parameters["Hospital cost outcome 1 Age 0 to 1"]
        + parameters["Hospital cost outcome 2 Age 0 to 1"]
        + parameters["Hospital cost outcome 4 Age 0 to 1"]
        + parameters["Hospital cost outcome 5 Age 0 to 1"]
        + parameters["Hospital cost outcome 6 Age 0 to 1"]
        + parameters["Hospital cost outcome 7 Age 0 to 1"]
        + parameters["Hospital cost outcome 8 Age 0 to 1"]
    )
    
    results["Total cost children"] = (
        results["DALYs children, in USD"]
        + results["Income loss children"]
        + results["Hospital cost children"]
    )

    results["Total DALYs, in USD"] = (
        results["DALYs children, in USD"]
        + results["DALYs women, in USD"]
    )

    results["Total income loss"] = (
        results["Income loss women"]
        + results["Income loss children"]
    )

    results["Total cost"] = (
        results["Total cost women"]
        + results["Total cost children"]
    )

    return results
