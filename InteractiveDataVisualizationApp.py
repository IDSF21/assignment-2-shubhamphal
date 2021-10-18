from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go


#country_vaccinations = pd.read_csv('country_vaccinations.csv')
#country_vaccinations_by_manufacturer = pd.read_csv('country_vaccinations_by_manufacturer.csv')
def get_vaccine_statistics(data,date):
    return data[data['date'] == date]

@st.cache
def get_country_coordinates():
    country_coordinates ='world-countries.json'
    return country_coordinates
@st.cache
def load_vaccine_manufacturer_data() -> pd.DataFrame:
    df = pd.read_csv('country_vaccinations_by_manufacturer.csv')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df

@st.cache
def load_vaccination_data() -> pd.DataFrame:
    df = pd.read_csv('country_vaccinations.csv')
    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
    countries = df['country'].unique().tolist()
    return df, countries

def total_vaccination_by_country(df) -> pd.DataFrame:
    total_vaccination=df.groupby(['iso_code'],group_keys = False).agg({'date': 'max','total_vaccinations':'max'}).reset_index()
    return total_vaccination

@st.cache
def initialize_repository():
    repository={}
    vaccination_data, countries = load_vaccination_data()
    manufacturer_data = load_vaccine_manufacturer_data()
    country_coordinates = get_country_coordinates()
    total_vaccinations  = total_vaccination_by_country(vaccination_data)
    repository['vaccination_data'] = vaccination_data
    repository['countries'] = countries
    repository['manufacturer_data'] = manufacturer_data
    return repository


def get_country_data(data,country):
    data=data[data['country']== country].copy()
    return data[['date','total_vaccinations','total_vaccinations_per_hundred','people_fully_vaccinated','people_fully_vaccinated_per_hundred','people_vaccinated_per_hundred','people_vaccinated','daily_vaccinations','vaccines','source_name']]

def get_topk_vaccine_distribution_by_manufacturer(data,k,date):
    data = data[data['date'] < str(date)]
    data = data.groupby(['location','vaccine'],group_keys = False).agg({'total_vaccinations':'max'}).reset_index()
    topk_countries = data.groupby(['location'],group_keys = False).agg({'total_vaccinations':'sum'}).reset_index().sort_values('total_vaccinations',ascending = False)['location'].iloc[0:k].tolist()
    data = data[data['location'].isin(topk_countries)]
    return data

def get_formatted_key(key):
    if key == 'total vaccines administered':
        result = 'total_vaccinations'
    elif key == 'total vaccines administered per hundred':
        result = 'total_vaccinations_per_hundred'
    elif key == 'people vaccinated':
        result = 'people_vaccinated'
    elif key == 'people vaccinated per hundred':
        result = 'people_vaccinated_per_hundred' 
    elif key == 'people fully vaccinated':
        result = 'people_fully_vaccinated'
    elif key == 'people fully vaccinated per hundred':
        result = 'people_fully_vaccinated_per_hundred'
    elif key =='daily vaccinations':
        result = 'daily_vaccinations'
    else:
        result = 'total_vaccinations'
    return result  


def get_global_vaccination_data(data,trend_date,key='total_vaccinations')-> pd.DataFrame:
    key = get_formatted_key(key)
    data = data[data['date'] < str(trend_date)]
    df = data.groupby(['iso_code','country'],group_keys= False).agg({key:'max'}).reset_index()
    return df, key

def get_summary_statistics_global(data):
    data = data.groupby(['iso_code','country'],group_keys= False).agg({'people_fully_vaccinated_per_hundred':'max','total_vaccinations_per_hundred':'max'}).reset_index()
    total_people_vaccinated = data['total_vaccinations_per_hundred'].mean()
    total_fully_vaccinated = data['people_fully_vaccinated_per_hundred'].mean()
    return total_people_vaccinated,total_fully_vaccinated


def get_summary_statistics_country(data):
    total_people_vaccinated = data['total_vaccinations_per_hundred'].max()
    fully_vaccinated = data['people_fully_vaccinated_per_hundred'].max()
    return total_people_vaccinated,fully_vaccinated


def get_popular_vaccines(data):
    l1=data['vaccines'].unique().tolist()
    vaccines = set()
    for ele in l1:
        vaccines=vaccines.union(set(ele.split(',')))
    return list(vaccines)


def get_summary_statistics_vaccintation_data(data):
    summary = {}
    vaccination_summary=data.groupby(['iso_code'],group_keys = False).agg({'date': 'max','total_vaccinations':'max','people_fully_vaccinated':'max'}).reset_index()
    summary['total_vaccinations'] = vaccination_summary['total_vaccinations'].sum()
    summary['people_fully_vaccinated'] = vaccination_summary['people_fully_vaccinated'].sum()
    return summary

def get_summary_statistics_vaccines_manufactured(data):
    vaccines_manufactured = data.groupby(['location','vaccine'],group_keys = False).agg({'date': 'max','total_vaccinations':'max'}).reset_index()
    return vaccines_manufactured.groupby(['vaccine'],group_keys = False).agg({'total_vaccinations':'sum'}).reset_index()


def run():
    st.set_page_config(
        page_title="Covid-19 Vaccine Dashboard",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Data containing vaccine distribution by different manufacturers"
        }
    )
    repository = initialize_repository()
    st.sidebar.title('Covid-19 Vaccine Analytics')
    st.session_state.workflow = st.sidebar.radio("Select Granularity:", ('Global level','Country level'),index=0)

    st.sidebar.write("""
    This project was developed as part of the coursework for
    05-839 Interactive Data Science course offered at CMU by Shubham Phal.
    The dataset used for this project can be found on [Kaggle](https://www.kaggle.com/gpreda/covid-world-vaccination-progress). 
    This application utilizes data collected upto 9 October 2021
    """)



    if st.session_state.workflow == 'Country level':
        st.title("Countrywise Vaccine Analytics")
        st.write("")
        country = st.selectbox("Select a Country", repository['countries']).strip()
        country_wise_data = get_country_data(repository['vaccination_data'],country)
        total_vaccines_given, total_fully_vaccinated = get_summary_statistics_country(country_wise_data)
        avg_people_vaccinated,avg_fully_vaccinated = get_summary_statistics_global(repository['vaccination_data'])


        m1, m2 = st.columns((2,2))
        #m1.write('')
        m1.metric(label ='Total Vaccines Administered per Hundred',value = int(total_vaccines_given), delta = str(int(total_vaccines_given-avg_people_vaccinated))+" Compared to average")
        m2.metric(label ='People fully Vaccinated per Hundred',value = int(total_fully_vaccinated), delta = str(int(total_fully_vaccinated-avg_fully_vaccinated))+" Compared to average")
        #m1.write('')
        popular_vaccines = get_popular_vaccines(country_wise_data)

        st.write("")
        st.write("Vaccines in use "+', '.join(popular_vaccines))
        st.write("")

        st.write("#### Daily vaccination rate")
        fig=px.area(country_wise_data, x=country_wise_data.date, y=country_wise_data.daily_vaccinations)
        fig.update_xaxes(title_text='date',rangeslider_visible=True)
        fig.update_yaxes(title_text='total vaccinataion')
        st.plotly_chart(fig)
        st.write("#### Compare With")


        row33_spacer1, row33_1, row33_spacer2, row33_2   = st.columns((.2, 3.2, .2, 2.5))
        with row33_1:
            metric = st.selectbox("Select a metric",["daily vaccinations","total vaccines administered","total vaccines administered per hundred","people vaccinated","people vaccinated per hundred","people fully vaccinated","people fully vaccinated per hundred"]) 
            metric = get_formatted_key(metric)
        with row33_2:
            selected_country_options = st.multiselect("Select one or more countries to compare with:",repository['countries'])
        dispfig = go.Figure()
        dispfig.add_trace(go.Scatter(x=country_wise_data.date, y=country_wise_data[metric], fill='tozeroy',
                    mode='lines', name = country # override default markers+lines
                    ))
        for country_option in selected_country_options:
            country_option_data = get_country_data(repository['vaccination_data'],country_option)
            dispfig.add_trace(go.Scatter(x=country_option_data.date, y=country_option_data[metric], fill='tonexty',
                    mode= 'lines',name=country_option))
        st.plotly_chart(dispfig)

        st.write("")
        st.write("#### "+country+" Vaccine Data")
        st.write("")
        
        st.dataframe(country_wise_data.astype(str).replace('nan','No Data Available').style.applymap(lambda x: "background-color: red" if x=='No Data Available' else "background-color: None"))
        #dispfig.show()



    else:
        st.title("Global Covid-19 Vaccine Analytics")
        st.write("")
        st.write("")


        summary = get_summary_statistics_vaccintation_data(repository['vaccination_data'])
        manufacturer_data = get_summary_statistics_vaccines_manufactured(repository['manufacturer_data'])

        #with row43_1:
        total_stat = "{:,}".format(int(summary['total_vaccinations']))
        people_stat = "{:,}".format(int(summary['people_fully_vaccinated']))
        manufacturer_data =manufacturer_data.sort_values(by='total_vaccinations',ascending=False)
        popular_vaccine = manufacturer_data['vaccine'].iloc[0].split('/')[0]
            #st.write("Total Vaccines Given ",total_stat)
        
        m3, m4, m5= st.columns((4,4,4))
            #m1.write('')
        m3.metric(label ='Total Vaccines Administered',value = total_stat)
        m4.metric(label ='People Fully Vaccinated ',value = people_stat)
        m5.metric(label ='Most Popular Vaccine ',value = popular_vaccine)


        st.write("")
        st.write('#### Vaccination Trends')
        st.write("")
        st.write("")
        row23_spacer1, row23_1, row23_spacer2, row23_2, row23_spacer3, row23_3, row23_spacer4   = st.columns((.2, 2.3, .2, 6, .2, 2.3, .2))

        with row23_1:
            trends_date = st.date_input('Date until',key="trends")
        with row23_2:
            key = st.selectbox ("Color by", ["total vaccines administered","total vaccines administered per hundred","people vaccinated","people vaccinated per hundred","people fully vaccinated","people fully vaccinated per hundred"],key="trends_selection") 


        map_data, map_key = get_global_vaccination_data(repository['vaccination_data'],trends_date,key)
        global_fig = px.choropleth(map_data,width=800,height=600,locations="iso_code",color=map_key, hover_name="country",color_continuous_scale=px.colors.sequential.Purpor)
        #global_fig.update_traces(geo_bgcolor="#323130")

        global_fig.update_geos(projection_type="orthographic")
        global_fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0},geo=dict(bgcolor= 'rgba(128,128,128,0)'))
        st.plotly_chart(global_fig)



        st.write("")
        st.write("")
        ##Vaccine Distribution
        st.write('#### Vaccine Distribution by Manufacturer')
        #Top 10 stacked horizontal column chart
        row13_spacer1, row13_1, row13_spacer2, row13_2, row13_spacer3, row13_3, row13_spacer4   = st.columns((.2, 2.3, .2, 2.3, .2, 2.3, .2))
        k =5

        with row13_1:
            date = st.date_input('Date until',key="manufacturers")
        with row13_2:
            k = st.selectbox ("Top k regions", [5,10,15,20,25,30,35],key="") 

        vaccine_distribution_data = get_topk_vaccine_distribution_by_manufacturer(repository['manufacturer_data'],k,date)
        fig = px.bar(vaccine_distribution_data, x="total_vaccinations", y="location", color='vaccine', orientation='h',
             hover_data=["vaccine", "total_vaccinations"],
             width = 800,
             height=600,
             title='Region wise distribution')     

        fig.update_xaxes(title_text='total vaccination')
        fig.update_yaxes(title_text='region')     
        fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig)


        st.write("")
        st.write("")
        st.write('###### Distribution Statistics')
        st.dataframe(manufacturer_data.rename(columns = {'total_vaccinations':'Total Doses Administered'}))



        


if __name__ == '__main__':
    run()