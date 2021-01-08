import altair as alt
import streamlit as st
import pandas as pd

def app():
    ##########################################################
    #############       smoking_deaths.py        #############
    ##########################################################
    st.title("Tobacco: a silent killer")
    # st.header("")
    
    @st.cache(allow_output_mutation=True)
    def load_data():
        deaths = pd.read_csv('data/smoking-deaths-by-age.csv',
                            header=0,
                            names=[
                                'country',
                                'code',
                                'year',
                                '15 to 49',
                                '50 to 69',
                                'Above 70'])
        factors = pd.read_csv('data/number-of-deaths-by-risk-factor.csv',
                            header=0,
                            index_col=False,
                            names=[
                                'country',
                                'code',
                                'year',
                                'Diet low in vegetables',
                                'Diet low in whole grains',
                                'Diet low in nuts and seeds',
                                'Diet low in calcium',
                                'Unsafe sex',
                                'No access to handwashing facility',
                                'Child wasting',
                                'Child stunting',
                                'Diet high in red meat',
                                'Diet low in fiber',
                                'Diet low in seafood omega-3 fatty acids',
                                'Diet high in sodium',
                                'Low physical activity',
                                'Non-exclusive breastfeeding',
                                'Discontinued breastfeeding',
                                'Iron deficiency',
                                'Vitamin A deficiency',
                                'Zinc deficiency',
                                'Smoking',
                                'Secondhand smoke',
                                'Alcohol use',
                                'Drug use',
                                'High fasting plasma glucose',
                                'High total cholesterol', # Many null values
                                'High systolic blood pressure',
                                'High body-mass index',
                                'Low bone mineral density',
                                'Diet low in fruits',
                                'Diet low in legumes',
                                'Low birth weight for gestation',
                                'Unsafe water source',
                                'Unsafe sanitation',
                                'Household air pollution from solid fuels',
                                'Air pollution',
                                'Outdoor air pollution'])

        # Convert data from wide to long
        deaths = pd.melt(deaths, id_vars=['country', 'year'], value_vars=['15 to 49', '50 to 69', 'Above 70'], var_name='Age')
        factors = pd.melt(factors, id_vars=['country', 'year'], value_vars=['Diet low in vegetables',
                                'Diet low in nuts and seeds',
                                'Diet low in calcium',
                                'Unsafe sex',
                                'No access to handwashing facility',
                                'Child wasting',
                                'Child stunting',
                                'Diet high in red meat',
                                'Diet low in fiber',
                                'Diet low in seafood omega-3 fatty acids',
                                'Diet high in sodium',
                                'Low physical activity',
                                'Non-exclusive breastfeeding',
                                'Discontinued breastfeeding',
                                'Iron deficiency',
                                'Vitamin A deficiency',
                                'Zinc deficiency',
                                'Smoking',
                                'Secondhand smoke',
                                'Alcohol use',
                                'Drug use',
                                'High fasting plasma glucose',
                                'High total cholesterol', # Many null values
                                'High systolic blood pressure',
                                'High body-mass index',
                                'Low bone mineral density',
                                'Diet low in fruits',
                                'Diet low in legumes',
                                'Low birth weight for gestation',
                                'Unsafe water source',
                                'Unsafe sanitation',
                                'Household air pollution from solid fuels',
                                'Air pollution',
                                'Outdoor air pollution'], var_name='risk_factor')

        countries = deaths['country'].unique() # get unique country names
        countries.sort() # sort alphabetically
        minyear = deaths.loc[:, 'year'].min()
        maxyear = deaths.loc[:, 'year'].max()
        return deaths, factors, countries, minyear, maxyear

    deaths, factors, countries, minyear, maxyear = load_data()

    # Country Selection
    selectCountry = st.selectbox('Select a country: ', countries, 73)


    # Year selection
    slider = st.slider('Select a period of time', int(str(minyear)), int(str(maxyear)), (1990, 2017))

    # brush = alt.selection_interval(encodings=['x'])
    # years = alt.Chart(deaths).mark_line().add_selection(
    #     brush
    # ).transform_filter(
    #     alt.datum.country == selectCountry
    # ).encode(
    #     alt.X('year:O', title='Year'),
    #     alt.Y('sum(value)', title='Smoking Deaths (all ages)')
    # ).properties(
    #     width=600,
    #     height=150
    # )

    # Area chart - Smoking deaths by ages
    base = alt.Chart(deaths, title='Smoking deaths by age').mark_bar().transform_filter(
        {'and': [{'field': 'country', 'equal': selectCountry},
                {'field': 'year', 'range': slider}]}
    ).encode(
        alt.X('year:O', title='Year'),
        y=alt.Y('value:Q', title='Number of smoking deaths'),
        color=alt.Color('Age:O', scale=alt.Scale(scheme='lightorange')),
        tooltip=alt.Tooltip(["value:Q"],format=",.0f",title="Deaths"),
        # alt.Tooltip(aggregate='sum', field="value", formatType="number"),

        text='Age:O'
    ).properties(
        width=780,
        height=350
    )

    # Bar chart - Risk factors
    bar_factors = alt.Chart(factors, title='Ranking of the top 20 risk factors').mark_bar().transform_filter(
        {'and': [{'field': 'country', 'equal': selectCountry},
                {'field': 'year', 'range': slider}]}
    ).transform_aggregate(
        sum_deaths='sum(value)',
        groupby=["risk_factor"]
    ).transform_window(
        rank='rank(sum_deaths)',
        sort=[alt.SortField('sum_deaths', order='descending')]
    ).transform_filter(
        alt.datum.rank < 20
    ).encode(
        alt.X('sum_deaths:Q', title='Total deaths over the period of time'),
        y=alt.Y('risk_factor:O',sort='-x', title='Risk factor'),
        tooltip=alt.Tooltip(["sum_deaths:Q"],format=",.0f",title="Deaths"),
        color=alt.condition(
          alt.datum['risk_factor'] == 'Smoking',
          alt.value("red"),  # Smoking color
          alt.value("lightgray")  # Other than smoking
        )
    ).properties(
        width=700,
        height=350
    )

    container1 = st.beta_container()
    with container1:
        st.altair_chart(base)

    st.markdown("Smoking is a critical factor leading to deaths, especially for old people. The number of people aged over 70 who died because of smoking is extremely high in all countries.")
    st.markdown("In the bar chart below, we can see how smoking ranks in the list of top 20 risk factors that lead to deaths in the chosen country in the chosen period of time.")

    st.altair_chart(bar_factors)
    # Visualize
    # st.altair_chart(alt.hconcat(alt.vconcat(base,years)
    #                             .properties(spacing=20), bar_factors)
    #                             .configure_legend(orient='top-left', strokeColor='gray',
    #                                             fillColor='#EEEEEE',
    #                                             padding=5,
    #                                             cornerRadius=10)
    #                             .properties(spacing=20, autosize="pad")
    #                             .configure_title(
    #                                             align="center",
    #                                             fontSize=20,
    #                                             font='Arial',
    #                                             color='black')) 