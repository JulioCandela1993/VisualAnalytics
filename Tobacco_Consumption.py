import streamlit as st
import pandas as pd
import altair as alt

st.title("Tobacco: a silent killer")

'''
Bla bla bla
'''

st.header("How are countries controlling Tobacco consumption?")

'''
The following analysis is based on the evaluation made by World Health Organization (WHO) to country policies against Tobacco. A score from 1 to 5 is assigned depending on the intensity of a country to deal with Tobacco issues being 1 the worst and 5 the best
'''


with st.echo():
	dataset = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/cars.json'
	movies = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/movies.json'
	sp500 = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/sp500.csv'
	stocks = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/stocks.csv'
	flights = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/flights-5k.json'

st.header("Introducing Selections")

import json
import requests
import numpy as np

filtered_data = pd.DataFrame(np.array([["Peru", 30],["Chile",10]]), columns = ["Country", "Value"])

url_topojson = 'https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json'
data_topojson_remote = alt.topo_feature(url=url_topojson, feature='countries1')
map_geojson = alt.Chart(data_topojson_remote).mark_geoshape(
    stroke="black",
    strokeWidth=1,
    fill='lightgray'
).properties(
    width=800,
    height=800
)
    
choro = alt.Chart(data_topojson_remote).mark_geoshape(
    stroke='black'
).encode(
    color="Value:Q",
            tooltip=[
                alt.Tooltip("properties.name:O", title="Country name"),
                alt.Tooltip("Value:Q", title="Indicator value"),
            ],
).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(filtered_data, "Country", ["Value"]),
    )

st.altair_chart(map_geojson + choro)


