import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any
import streamlit as st

from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from utils import format_large_number
from utils import format_large_number_long

#COLOURS
# Teal #00636b
# Purple #63295c
# Turquoise #00C3BB
# Blue #333085
# Yellow #ffd400
# Red #d61f3d
# Light #efefef
# Text #3d3d3b



def display_cost_overview(parameters: Dict[str, Any]):

    #total_cost_in_billion = (parameters["Total cost"] / 1000000000) * parameters["conversion_rate"]
    total_cost = format_large_number_long(parameters["Total cost"] * parameters["conversion_rate"])
    mother_percentage = (parameters["Total cost women"] / parameters["Total cost"]) * 100
    child_percentage = (parameters["Total cost children"] / parameters["Total cost"]) * 100

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"""
        <div style='text-align: left;'>
            <p style='font-size: 30px; color: #888; margin-bottom: 0;'>Total Cost</p>
            <p style='font-size: 54px; font-weight: bold; margin: 0; color: #262730;'>{parameters["currency_code"]}{" "}{total_cost}</p>
        </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='text-align: left;'>
            <p style='font-size: 16px; margin: 8px 0;'>Of these costs:</p>
            <p style='font-size: 18px; margin: -4px 0;'><span style='font-size: 28px; font-weight: bold;'>{mother_percentage:,.0f}%</span> relate to the mother</p>
            <p style='font-size: 18px; margin: -5px 0;'><span style='font-size: 28px; font-weight: bold;'>{child_percentage:,.0f}%</span> relate to the child</p>
        </div>
    """, unsafe_allow_html=True)


def render_cost_types_piechart(parameters: Dict[str, float]):

    dalys = round(parameters["Total DALYs, in USD"] * parameters["conversion_rate"])
    dalys_mother = round(parameters["DALYs women, in USD"] * parameters["conversion_rate"])
    dalys_child = round(parameters["DALYs children, in USD"] * parameters["conversion_rate"])
    income_loss = round(parameters["Total income loss"] * parameters["conversion_rate"])
    income_loss_mother = round(parameters["Income loss women"] * parameters["conversion_rate"])
    income_loss_child = round(parameters["Income loss children"] * parameters["conversion_rate"])
    hospital_cost = round(parameters["Hospital cost children"] * parameters["conversion_rate"])
    total_cost = round(parameters["Total cost"] * parameters["conversion_rate"])

    
    formatted_dalys = format_large_number_long(dalys, parameters["currency_symbol"])
    formatted_income_loss = format_large_number_long(income_loss, parameters["currency_symbol"])
    formatted_hospital_cost = format_large_number_long(hospital_cost, parameters["currency_symbol"])

    options = {
        #"devicePixelRatio": 2,
        #"grid": {"left": "0%", "right": "0%", "bottom": "0%", "top": "0%"}, #"containLabel": True},
        "toolbox": {
            "right": "5%",
            "feature": {
                "saveAsImage": {
                    "show": True,
                    "title": "Download",
                    "name": "cost-breakdown-piechart",
                    "pixelRatio": 3,
                    "backgroundColor": "#fff"
                }
            }
        },
        "tooltip": {
            "show": False,  # Disable tooltips completely
            "trigger": "item",
            "formatter": "{b}<br/>Value: ${c}<br/>{d}%",
            "confine": True,
            "textStyle": {
                "width": 300,
                "overflow": "break"
            }
        },
        #"legend": {"orient": "vertical", "left": "left",},
        "series": [
            {
                #"name": "Name1",
                "type": "pie",
                "radius": "55%",
                "center": ["48%", "50%"],
                "data": [
                    {"value": dalys,
                        "name": f"Quality of life losses:\n{{bold|{formatted_dalys}}} ({round(dalys / total_cost * 100)}%)",
                        "tooltip": {
                            "formatter": f"<div style='max-width: 10px; white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'><b>DALYs: {round(dalys / total_cost * 100)}%</b><br/>Value: {parameters["currency_symbol"]}{dalys:,}<br/><b>{round(dalys_mother / dalys * 100)}%</b> of these costs are associated with the mother and <b>{round(dalys_child / dalys * 100)}%</b> with the child.<br/>"
                        },
                        "itemStyle": {
                            "color": "#00636b"
                        }
                    },
                    {"value": income_loss, 
                        "name": f"Productivity losses:\n{{bold|{formatted_income_loss}}} ({round(income_loss / total_cost * 100)}%)",
                        "tooltip": {
                            "formatter": f"<div style='max-width: 300px; white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'><b>Income loss: {round(income_loss / total_cost * 100)}%</b><br/>Value: {parameters["currency_symbol"]}{income_loss:,}<br/><b>{round(income_loss_mother / income_loss * 100)}%</b> of these costs are associated with the mother and <b>{round(income_loss_child / income_loss * 100)}%</b> with the child.<br/>"
                        },
                        "itemStyle": {
                            "color": "#63295c"
                        }
                    },
                    {"value": hospital_cost,
                        "name": f"Healthcare costs:\n{{bold|{formatted_hospital_cost}}} ({round(hospital_cost / total_cost * 100)}%)",
                        "tooltip": {
                            "formatter": f"<div style='max-width: 300px; white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'><b>Hospital costs: {round(hospital_cost / total_cost * 100)}%</b><br/>Value: {parameters["currency_symbol"]}{hospital_cost:,}<br/><b>100%</b> of these costs are associated with the child.<br/>"
                        },
                        "itemStyle": {
                            "color": "#00C3BB"
                        }
                    }
                ],
                "label": {
                    "fontSize": 24,
                    "lineHeight": 26,
                    #"overflow": "break",
                    #"fontWeight": "bold",
                    "color": "#333",
                    #"position": "inside",
                    "formatter": "{b}",
                    "rich": {
                        "bold": {
                            "fontWeight": "bold",
                            "fontSize": 24,
                            "color": "#000"
                        }
                    }
                },
                "labelLine": {
                    "length": 20,
                    "length2": 20
                },
                "labelLayout": {
                    "width": 280,
                }
                #"emphasis": {
                #    "itemStyle": {
                #        "shadowBlur": 10,
                #        "shadowOffsetX": 0,
                #        "shadowColor": "rgba(0, 0, 0, 0.5)",
                #    }
                #},
            }
        ],
    }
    st_echarts(
        options=options,
        height="450px",
        renderer="svg"
    )


    
def render_costs_barchart_2(parameters: Dict[str, float]):

    # Health-related quality of life losses
    dalys = round(parameters["Total DALYs, in USD"] * parameters["conversion_rate"])
    dalys_mother = round(parameters["DALYs women, in USD"] * parameters["conversion_rate"])
    dalys_child = round(parameters["DALYs children, in USD"] * parameters["conversion_rate"])
    dalys_mother_depressed = round(parameters["DALYs women depressed, in USD"] * parameters["conversion_rate"])
    dalys_mother_anxious = round(parameters["DALYs women anxious, in USD"] * parameters["conversion_rate"])
    dalys_mother_suicide = round(parameters["DALYs women committing suicide ante and postnatal, in USD"] * parameters["conversion_rate"])

    # Productivity losses
    income_loss = round(parameters["Total income loss"] * parameters["conversion_rate"])
    income_loss_mother = round(parameters["Income loss women"] * parameters["conversion_rate"])
    income_loss_child = round(parameters["Income loss children"] * parameters["conversion_rate"])
    income_loss_mother_depressed = round(parameters["Income loss women depression"] * parameters["conversion_rate"])
    income_loss_mother_anxious = round(parameters["Income loss women anxiety"] * parameters["conversion_rate"])

    # Healthcare costs
    hospital_cost_mother = 0
    hospital_cost_child = round(parameters["Hospital cost children"] * parameters["conversion_rate"])

    total_cost = round(parameters["Total cost"] * parameters["conversion_rate"])

    js_formatter = JsCode(
        "function (value) {"
        " if (value >= 1e9) return (value / 1e9).toFixed(0) + 'B';"
        " if (value >= 1e6) return (value / 1e6).toFixed(0) + 'M';"
        " if (value >= 1e3) return (value / 1e3).toFixed(0) + 'K';"
        " return value;"
        "}"
    ).js_code

    options_multiple_stacks = {
        "toolbox": {
            "right": "5%",
            "feature": {
                "saveAsImage": {
                    "show": True,
                    "title": "Download",
                    "name": "cost-breakdown-barchart",
                    "pixelRatio": 2,
                    "backgroundColor": "#fff"
                }
            }
        },
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "show": False},
        "legend": {"show": False},  # Hide the legend
        #"legend": {"data": ["Mother Direct", "Mother Indirect", "Child Acute", "Child Chronic"]},
        "grid": {"left": "3%", "right": "8%", "bottom": "8%", "top": "0%", "containLabel": True},
        "xAxis": {"type": "value",
                  "name": parameters["currency_code"],
                  "nameLocation": "middle",
                  "nameGap": 30,
                  "axisLabel": {
                      "formatter": js_formatter
                      }
                  },
        "yAxis": {
            "type": "category",
            "data": ["Healthcare costs", "Productivity losses", "Health-related\nquality of life losses"],
            "axisLabel": {
                "fontSize": 16,
                "margin": 20,  # Distance from axis line to labels (default is 8)
                "align": "right",  # Align text to the right
                "verticalAlign": "middle"
            },
            "axisLine": {
                "show": True,
                "lineStyle": {"color": "#333"}
            },
            "z": 10
            },
        "series": [
            {
                "name": "Mother",
                "type": "bar",
                "stack": "mother",
                "data": [
                    {
                        "value": hospital_cost_mother, 
                        "itemStyle": {"color":"#00C3BB"},
                        #"label": {"show": True, "position": "right", "formatter": f"{0}% Mother"}
                        },
                    {
                        "value": income_loss_mother, 
                        "itemStyle": {"color": "#63295c"},
                        "label": {"show": True, "position": "right", 
                                  "formatter": f"{round(income_loss_mother / income_loss * 100)}% Mother",
                                  "fontSize": 13}
                        },
                    {
                        "value": dalys_mother,
                        "itemStyle": {"color": "#00636b"}, 
                        "label": {"show": True, "position": "right", "formatter": f"{round(dalys_mother / dalys * 100)}% Mother",
                                  "fontSize": 13}
                        }
                    ],
                
            },
            {
                "name": "Child",
                "type": "bar",
                "stack": "child",
                "data": [
                    {
                        "value": hospital_cost_child, 
                        "itemStyle": {"color":"#00C3BB"},
                        "label": {"show": True, "position": "right", "formatter": f"{100}% Child",
                                  "fontSize": 13}
                        },
                    {
                        "value": income_loss_child, 
                        "itemStyle": {"color": "#63295c"},
                        "label": {"show": True, "position": "right",
                                   "formatter": f"{round(income_loss_child / income_loss * 100)}% Child",
                                   "fontSize": 13}
                        },
                    {
                        "value": dalys_child,
                        "itemStyle": {"color": "#00636b"},
                        "label": {"show": True, "position": "right", "formatter": f"{round(dalys_child / dalys * 100)}% Child",
                                  "fontSize": 13}
                        }
                    ]
            },
        ]
    }

    st_echarts(
        options=options_multiple_stacks,
        height="400px",
        renderer="svg")
    




def render_costs_barchart_2_inside_right(parameters: Dict[str, float]):

    # Health-related quality of life losses
    dalys = round(parameters["Total DALYs, in USD"] * parameters["conversion_rate"])
    dalys_mother = round(parameters["DALYs women, in USD"] * parameters["conversion_rate"])
    dalys_child = round(parameters["DALYs children, in USD"] * parameters["conversion_rate"])
    dalys_mother_depressed = round(parameters["DALYs women depressed, in USD"] * parameters["conversion_rate"])
    dalys_mother_anxious = round(parameters["DALYs women anxious, in USD"] * parameters["conversion_rate"])
    dalys_mother_suicide = round(parameters["DALYs women committing suicide ante and postnatal, in USD"] * parameters["conversion_rate"])

    # Productivity losses
    income_loss = round(parameters["Total income loss"] * parameters["conversion_rate"])
    income_loss_mother = round(parameters["Income loss women"] * parameters["conversion_rate"])
    income_loss_child = round(parameters["Income loss children"] * parameters["conversion_rate"])
    income_loss_mother_depressed = round(parameters["Income loss women depression"] * parameters["conversion_rate"])
    income_loss_mother_anxious = round(parameters["Income loss women anxiety"] * parameters["conversion_rate"])

    # Healthcare costs
    hospital_cost_mother = 0
    hospital_cost_child = round(parameters["Hospital cost children"] * parameters["conversion_rate"])

    total_cost = round(parameters["Total cost"] * parameters["conversion_rate"])

    js_formatter = JsCode(
        "function (value) {"
        " if (value >= 1e9) return (value / 1e9).toFixed(0) + 'B';"
        " if (value >= 1e6) return (value / 1e6).toFixed(0) + 'M';"
        " if (value >= 1e3) return (value / 1e3).toFixed(0) + 'K';"
        " return value;"
        "}"
    ).js_code

    options_multiple_stacks = {
        "toolbox": {
            "right": "5%",
            "feature": {
                "saveAsImage": {
                    "show": True,
                    "title": "Download",
                    "name": "cost-breakdown-barchart",
                    "pixelRatio": 2,
                    "backgroundColor": "#fff"
                }
            }
        },
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "show": False},
        "legend": {"show": False},  # Hide the legend
        #"legend": {"data": ["Mother Direct", "Mother Indirect", "Child Acute", "Child Chronic"]},
        "grid": {"left": "3%", "right": "8%", "bottom": "8%", "top": "0%", "containLabel": True},
        "xAxis": {"type": "value",
                  "name": parameters["currency_code"],
                  "nameLocation": "middle",
                  "nameGap": 30,
                  "axisLabel": {
                      "formatter": js_formatter
                      }
                  },
        "yAxis": {
            "type": "category",
            "data": ["Healthcare costs", "Productivity losses", "Health-related\nquality of life losses"],
            "axisLabel": {
                "fontSize": 16,
                "margin": 20,  # Distance from axis line to labels (default is 8)
                "align": "right",  # Align text to the right
                "verticalAlign": "middle"
            },
            "axisLine": {
                "show": True,
                "lineStyle": {"color": "#333"}
            },
            "z": 10
            },
        "series": [
            {
                "name": "Mother",
                "type": "bar",
                "stack": "mother",
                "data": [
                    {
                        "value": hospital_cost_mother, 
                        "itemStyle": {"color":"#00C3BB"},
                        #"label": {"show": True, "position": "right", "formatter": f"{0}% Mother"}
                        },
                    {
                        "value": income_loss_mother, 
                        "itemStyle": {"color": "#63295c"},
                        "label": {"show": True, "position": "insideRight", 
                                  "formatter": f"{round(income_loss_mother / income_loss * 100)}% Mother",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        },
                    {
                        "value": dalys_mother,
                        "itemStyle": {"color": "#00636b"}, 
                        "label": {"show": True, "position": "insideRight", "formatter": f"{round(dalys_mother / dalys * 100)}% Mother",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        }
                    ],
                
            },
            {
                "name": "Child",
                "type": "bar",
                "stack": "child",
                "data": [
                    {
                        "value": hospital_cost_child, 
                        "itemStyle": {"color":"#00C3BB"},
                        "label": {"show": True, "position": "insideRight", "formatter": f"{100}% Child",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        },
                    {
                        "value": income_loss_child, 
                        "itemStyle": {"color": "#63295c"},
                        "label": {"show": True, "position": "insideRight",
                                   "formatter": f"{round(income_loss_child / income_loss * 100)}% Child",
                                   "fontSize": 13,
                                   "color": "#fff"}
                        },
                    {
                        "value": dalys_child,
                        "itemStyle": {"color": "#00636b"},
                        "label": {"show": True, "position": "insideRight", "formatter": f"{round(dalys_child / dalys * 100)}% Child",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        }
                    ]
            },
        ]
    }

    st_echarts(
        options=options_multiple_stacks,
        height="400px",
        renderer="svg")
    


def render_costs_barchart_2_inside_left(parameters: Dict[str, float]):

    # Health-related quality of life losses
    dalys = round(parameters["Total DALYs, in USD"] * parameters["conversion_rate"])
    dalys_mother = round(parameters["DALYs women, in USD"] * parameters["conversion_rate"])
    dalys_child = round(parameters["DALYs children, in USD"] * parameters["conversion_rate"])
    dalys_mother_depressed = round(parameters["DALYs women depressed, in USD"] * parameters["conversion_rate"])
    dalys_mother_anxious = round(parameters["DALYs women anxious, in USD"] * parameters["conversion_rate"])
    dalys_mother_suicide = round(parameters["DALYs women committing suicide ante and postnatal, in USD"] * parameters["conversion_rate"])

    # Productivity losses
    income_loss = round(parameters["Total income loss"] * parameters["conversion_rate"])
    income_loss_mother = round(parameters["Income loss women"] * parameters["conversion_rate"])
    income_loss_child = round(parameters["Income loss children"] * parameters["conversion_rate"])
    income_loss_mother_depressed = round(parameters["Income loss women depression"] * parameters["conversion_rate"])
    income_loss_mother_anxious = round(parameters["Income loss women anxiety"] * parameters["conversion_rate"])

    # Healthcare costs
    hospital_cost_mother = 0
    hospital_cost_child = round(parameters["Hospital cost children"] * parameters["conversion_rate"])

    total_cost = round(parameters["Total cost"] * parameters["conversion_rate"])

    js_formatter = JsCode(
        "function (value) {"
        " if (value >= 1e9) return (value / 1e9).toFixed(0) + 'B';"
        " if (value >= 1e6) return (value / 1e6).toFixed(0) + 'M';"
        " if (value >= 1e3) return (value / 1e3).toFixed(0) + 'K';"
        " return value;"
        "}"
    ).js_code

    options_multiple_stacks = {
        "toolbox": {
            "right": "5%",
            "feature": {
                "saveAsImage": {
                    "show": True,
                    "title": "Download",
                    "name": "cost-breakdown-barchart",
                    "pixelRatio": 2,
                    "backgroundColor": "#fff"
                }
            }
        },
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "show": False},
        "legend": {"show": False},  # Hide the legend
        #"legend": {"data": ["Mother Direct", "Mother Indirect", "Child Acute", "Child Chronic"]},
        "grid": {"left": "3%", "right": "8%", "bottom": "8%", "top": "0%", "containLabel": True},
        "xAxis": {"type": "value",
                  "name": parameters["currency_code"],
                  "nameLocation": "middle",
                  "nameGap": 30,
                  "axisLabel": {
                      "formatter": js_formatter
                      }
                  },
        "yAxis": {
            "type": "category",
            "data": ["Healthcare costs", "Productivity losses", "Health-related\nquality of life losses"],
            "axisLabel": {
                "fontSize": 16,
                "margin": 20,  # Distance from axis line to labels (default is 8)
                "align": "right",  # Align text to the right
                "verticalAlign": "middle"
            },
            "axisLine": {
                "show": True,
                "lineStyle": {"color": "#333"}
            },
            "z": 10
            },
        "series": [
            {
                "name": "Mother",
                "type": "bar",
                "stack": "mother",
                "data": [
                    {
                        "value": hospital_cost_mother, 
                        "itemStyle": {"color":"#00C3BB"},
                        #"label": {"show": True, "position": "right", "formatter": f"{0}% Mother"}
                        },
                    {
                        "value": income_loss_mother, 
                        "itemStyle": {"color": "#63295c"},
                        "label": {"show": True, "position": "insideLeft", 
                                  "formatter": f"{round(income_loss_mother / income_loss * 100)}% Mother",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        },
                    {
                        "value": dalys_mother,
                        "itemStyle": {"color": "#00636b"}, 
                        "label": {"show": True, "position": "insideLeft", "formatter": f"{round(dalys_mother / dalys * 100)}% Mother",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        }
                    ],
                
            },
            {
                "name": "Child",
                "type": "bar",
                "stack": "child",
                "data": [
                    {
                        "value": hospital_cost_child, 
                        "itemStyle": {"color":"#00C3BB"},
                        "label": {"show": True, "position": "insideLeft", "formatter": f"{100}% Child",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        },
                    {
                        "value": income_loss_child, 
                        "itemStyle": {"color": "#63295c"},
                        "label": {"show": True, "position": "insideLeft",
                                   "formatter": f"{round(income_loss_child / income_loss * 100)}% Child",
                                   "fontSize": 13,
                                   "color": "#fff"}
                        },
                    {
                        "value": dalys_child,
                        "itemStyle": {"color": "#00636b"},
                        "label": {"show": True, "position": "insideLeft", "formatter": f"{round(dalys_child / dalys * 100)}% Child",
                                  "fontSize": 13,
                                  "color": "#fff"}
                        }
                    ]
            },
        ]
    }

    st_echarts(
        options=options_multiple_stacks,
        height="400px",
        renderer="svg")