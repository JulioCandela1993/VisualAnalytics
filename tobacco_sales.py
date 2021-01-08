import altair as alt
import streamlit as st
import pandas as pd
import numpy as np


def app():
    @st.cache
    def load_data(sales_path, consumption_path):
        sales_data = pd.read_csv(sales_path,
                            header=0,
                            names=[
                                'Country',
                                'Code',
                                'Year',
                                'NumCig'
                            ],
                            dtype={'Country': str,
                                    'Code': str,
                                    'Year': 'Int64',
                                    'NumCig': 'float64'})
        consumption_data = pd.read_csv(consumption_path,
                            header=0,
                            names=[
                                'Country',
                                'Code',
                                'Year',
                                'NumCig'
                            ],
                            dtype={'Country': str,
                                    'Code': str,
                                    'Year': 'Int64',
                                    'NumCig': 'float64'}
                            )
        return sales_data, consumption_data

    sales_path = 'data/sales-of-cigarettes-per-adult-per-day.csv'
    consumption_path = 'data/consumption-per-smoker-per-day.csv'
    sales_data, consumption_data = load_data(sales_path, consumption_path)
    container = st.beta_container()
    with container:
        st.header('Tobacco sales trend in different countries')
        '''
        Below, you can see how sales and consumption of cigarettes changed over the years in different countries.
        The sales chart shows the average number of cigarettes sold per day per adult, the consumption chart
        displays the average number of cigarettes consumed daily per smoker.
        Use the year slider to choose a period to focus on and also select the countries of your interest.
        '''
        countries = st.multiselect('Select countries to plot',
                            sales_data.groupby('Country').count().reset_index()['Country'].tolist(),
                            default=['France', 'Germany', 'Spain'])

    # lower year bound
    min_year_sales = max(sales_data.loc[sales_data['Country'] == country]['Year'].min()
    for country in countries)
    min_year_consumption = max(consumption_data.loc[consumption_data['Country'] == country]['Year'].min()
    for country in countries)
    min_year = max(min_year_sales, min_year_consumption)

    # upper year bound
    max_year_sales = min(sales_data.loc[sales_data['Country'] == country]['Year'].max()
    for country in countries)
    max_year_consumption = min(sales_data.loc[sales_data['Country'] == country]['Year'].max()
    for country in countries)
    max_year = min(max_year_sales, max_year_consumption)

    slider = st.slider('Select a period to plot',
                        int(str(min_year)), 
                        int(str(max_year)),
                        (int(str(min_year)), int(str(max_year))))
                        
    sales_chart = alt.Chart(sales_data, height=300, width=500,
                            title='Sales of cigarettes per adult per day',
                            ).mark_line().encode(
                            alt.X('Year', axis=alt.Axis(title='Years', tickCount=5)),
                            alt.Y('NumCig', axis=alt.Axis(title='')),
                            alt.Color('Country')
                            ).transform_filter(
                                                {'and': [{'field': 'Country', 'oneOf': countries},
                                                        {'field': 'Year', 'range': slider}]}
                                                )
    consumption_chart = alt.Chart(consumption_data, height=300, width=500,
                                    title='Consumption per smoker per day').mark_line().encode(
                                        alt.X('Year', axis=alt.Axis(title='Years', tickCount=5)),
                                        alt.Y('NumCig', axis=alt.Axis(title='')),
                                        alt.Color('Country')
                                        ).transform_filter(
                                            {'and': [{'field': 'Country', 'oneOf': countries},
                                                    {'field': 'Year', 'range': slider}]}
                                            )

    # ruler
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Year'], empty='none')
    sales_selectors = alt.Chart(sales_data).mark_point().encode(
        x='Year:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    ).transform_filter({'and': [{'field': 'Country', 'oneOf': countries},
                {'field': 'Year', 'range': slider}]})
    sales_points = sales_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    sales_text = sales_chart.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'NumCig:Q', alt.value(' '), format='.1f')
    )
    sales_rules = alt.Chart(sales_data).mark_rule(color='gray').encode(
        x='Year:Q',
    ).transform_filter(
        nearest
    )

    consumption_selectors = alt.Chart(consumption_data).mark_point().encode(
        x='Year:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    ).transform_filter({'and': [{'field': 'Country', 'oneOf': countries},
                {'field': 'Year', 'range': slider}]})
    consumption_points = consumption_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    consumption_text = consumption_chart.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'NumCig:Q', alt.value(' '), format='.1f')
    )
    consumption_rules = alt.Chart(consumption_data).mark_rule(color='gray').encode(
        x='Year:Q',
    ).transform_filter(
        nearest
    )



    with container:

        
        sales_chart = alt.layer(
        sales_chart, sales_selectors, sales_points, sales_rules, sales_text
        )
        consumption_chart = alt.layer(
        consumption_chart, consumption_selectors, consumption_points, consumption_rules, consumption_text
        )
        st.altair_chart(alt.hconcat(sales_chart, consumption_chart))

st.set_page_config(layout="wide")
app()