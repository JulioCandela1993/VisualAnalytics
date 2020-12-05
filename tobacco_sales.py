import altair as alt
import streamlit as st
import pandas as pd


sales_data = pd.read_csv('data/sales-of-cigarettes-per-adult-per-day.csv',
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


sales_bycountry = st.multiselect('Country',
                           sales_data.groupby('Country').count().reset_index()['Country'].tolist())
sales_minyear = sales_data.loc[:, 'Year'].min()
sales_maxyear = sales_data.loc[:, 'Year'].max()

sales_slidermin = alt.binding_range(min=sales_minyear, max=sales_maxyear, name='Year')
sales_slidermax = alt.binding_range(min=sales_minyear, max=sales_maxyear, name='Year')
sales_selector = alt.selection_single(name='Year', bind=sales_slidermax, fields=['Year'])

sales_chart = alt.Chart(sales_data).mark_line().encode(
    alt.X('Year'),
    alt.Y('NumCig'),
    alt.Color('Country')
).transform_filter(
    {"field": "Country", "oneOf": sales_bycountry}
    ).add_selection(sales_selector).interactive()
# {"field": "Country", "oneOf": sales_bycountry}, 
#{"and": [{"field": "Year", "oneOf": [sales_selector.Year]}]}
print(type(sales_selector.Year))
st.altair_chart(sales_chart)