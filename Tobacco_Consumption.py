import streamlit as st
import pandas as pd
import altair as alt

st.title("Tobacco: a silent killer")

'''
Bla bla bla
'''

st.header("How are countries controlling Tobacco consumption?")

'''
The following analysis is based on the evaluation made by World Health Organization (WHO) 
to country policies against Tobacco. A score from 1 to 5 is assigned depending on the intensity 
of a country to deal with Tobacco issues being 1 the worst and 5 the best
'''


control_dataset = 'https://raw.githubusercontent.com/JulioCandela1993/VisualAnalytics/master/control_policy.csv'

st.header("Intensity of controls per country")

import json
import requests
import numpy as np


#filtered_data = pd.DataFrame(np.array([["Peru", 30],["Chile",10]]), columns = ["Country", "Value"])


#data=pd.read_csv(control_dataset)


slider = alt.binding_range(min=2006, max=2012, step=1)
select_year = alt.selection_single(name="year", fields=['year'],
                                   bind=slider, init={'year': 2006})

url_topojson = 'https://raw.githubusercontent.com/JulioCandela1993/VisualAnalytics/master/world-countries.json'
data_topojson_remote = alt.topo_feature(url=url_topojson, feature='countries1')
map_geojson = alt.Chart(data_topojson_remote).mark_geoshape(
    stroke="black",
    strokeWidth=1,
    fill='lightgray'
).encode(
    color="Monitor:Q",
).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(control_dataset, "Country", ["Monitor","Year"])
).properties(
    width=800,
    height=400
)
    
choro = alt.Chart(data_topojson_remote).mark_geoshape(
    stroke='black'
).encode(
    color="Monitor:Q",
            tooltip=[
                alt.Tooltip("properties.name:O", title="Country name"),
                alt.Tooltip("Monitor:Q", title="Monitor"),
                alt.Tooltip("year:Q", title="Year"),
            ],
).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(control_dataset, "Country", ["Monitor","Year"])
).transform_calculate(
    year='parseInt(datum.Year)',
).add_selection(
    select_year
).transform_filter(
    select_year
)
    # .transform_filter(select_year)

st.altair_chart(map_geojson + choro)


