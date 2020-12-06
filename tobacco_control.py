import streamlit as st
import pandas as pd
import altair as alt
import json
import requests
import numpy as np

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


control_dataset = 'https://raw.githubusercontent.com/JulioCandela1993/VisualAnalytics/master/data/control_policy.csv'
deaths_dataset = 'https://raw.githubusercontent.com/JulioCandela1993/VisualAnalytics/master/data/deaths.csv'


#filtered_data = pd.read_csv(control_dataset)

#print(len(filtered_data))

st.header("Intensity of controls per country")

slider = alt.binding_range(min=2008, max=2018, step=2)
select_year = alt.selection_single(name="year", fields=['year'],
                                   bind=slider, init={'year': 2018})
#print(select_year)
control_metrics = ["Monitor",	
           "Protect from tobacco smoke",	
           "Offer help to quit tobacco use", 
           "Warn about the dangers of tobacco",
           "Enforce bans on tobacco advertising",
           "Raise taxes on tobacco",
           "Anti-tobacco mass media campaigns"
]



cols = st.selectbox('Control Measure', control_metrics)

if cols in control_metrics:   
    metric_to_show_in_covid_Layer = cols +":Q"
    metric_name = cols
   
years = ['2008', '2010', '2012', '2014', '2016', '2018']
columns_year = [metric_name+" "+str(year) for year in years]
columns = ["d" +str(year) for year in years]

url_topojson = 'https://raw.githubusercontent.com/JulioCandela1993/VisualAnalytics/master/world-countries.json'
data_topojson_remote = alt.topo_feature(url=url_topojson, feature='countries1')



map_geojson = alt.Chart(data_topojson_remote).mark_geoshape(
    stroke="black",
    strokeWidth=1,
    fill='lightgray'
).encode(
    color=metric_to_show_in_covid_Layer,
).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(control_dataset, "Country", [metric_name,"Year"])
).properties(
    width=800,
    height=400
)
    
    
choro = alt.Chart(data_topojson_remote).mark_geoshape(
    stroke='black'
).encode(
    color=metric_to_show_in_covid_Layer,
            tooltip=[
                alt.Tooltip("properties.name:O", title="Country name"),
                alt.Tooltip(metric_to_show_in_covid_Layer, title=metric_name),
                alt.Tooltip("year:Q", title="Year"),
                alt.Tooltip("key_val:N", title="d2008"),
            ],
).transform_calculate(
    d2008 = "1",
    d2010 = "1",
    d2012 = "1",
    d2014 = "1",
    d2016 = "1",
    d2018 = "1"
).transform_fold(
    columns, as_=['year', 'metric']
).transform_calculate(
    yearQ = 'replace(datum.year,"d","")'
).transform_calculate(
    key_val = 'datum.properties.name + datum.yearQ'
).transform_lookup(
        lookup="key_val",
        from_=alt.LookupData(control_dataset, "ID", [metric_name,"Year"])
).transform_calculate(
    year='parseInt(datum.Year)',
).add_selection(
    select_year
).transform_filter(
    select_year
)
    # .transform_filter(select_year)

st.altair_chart(map_geojson + choro)





circle_countries = alt.Chart(control_dataset).mark_circle(
    opacity=0.8,
    stroke='black',
    strokeWidth=1
).encode(
    alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
    alt.Y('Country:N', sort='-y'),
    alt.Size(metric_to_show_in_covid_Layer,
        scale=alt.Scale(range=[1, 1000]),
        legend=alt.Legend(title=metric_name)
    ),
    alt.Color('Country:N', legend=None)
).properties(
    width=800,
    height=400
).transform_lookup(
        lookup="Country",
        from_=alt.LookupData(deaths_dataset, "Country", ["deaths"])
).transform_calculate(
    deaths='parseFloat(datum.deaths)',
).transform_window(
    rank='rank(deaths)',
    sort=[alt.SortField('deaths', order='descending')]
).transform_filter(
    (alt.datum.rank < 60)
)

st.altair_chart(circle_countries)