from urllib.parse import uses_fragment
import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt


st.title("**Analysis of COVID-19 Vaccination**")


st.markdown('*<p>Hey   There! <br> Welcome To My Project. </p>*',unsafe_allow_html=True)
st.image('abc.jpg', use_column_width=True)
st.markdown('<p>This Project Visualizes the progress of Covid-19 Vaccination all over the world. <br>Covid-19 is an infectious disease which is caused by the coronavirus. The people getting affected by it will experience mild respiratory illness,fever, cold or stomach upset but will recover without requiring any special treatment. Whereas people who already have some medical issues from before or thr older people aremore prone to it and if they catch covid-19 then they need special treatment to recover from it. It is necessary to know how it spreads and what precautions need to be taken to be safe. It spreads through saliva droplets and discharge from the infected person nose when they sneezes or coughs.</p>', unsafe_allow_html=True)
st.markdown('<h1>Vaccination Dataset</h1>',unsafe_allow_html=True)
st.markdown('I found this dataset on Kaggle.')
st.balloons()
sidebar = st.sidebar
sidebar.title('Covid-19 Vaccination Data Visualization')



df=pd.read_csv ('country_vaccinations.csv')
vbm=pd.read_csv('country_vaccinations_by_manufacturer.csv')
wp=pd.read_csv('2021_population.csv')
st.dataframe(df)
countries = df.country.unique()
selCon = sidebar.selectbox(label="Select Vaccine Group", options=countries)
sidebar.checkbox('Confirm')
sidebar.button("Submit")

wp_sort = wp[['country', '2021_last_updated']] 
wp_sort.sort_values('country') 
vcn_drop = df.drop_duplicates('country', keep = "last") 
vcn_sort = vcn_drop[['country', 'people_fully_vaccinated']]
df_same = pd.concat([wp_sort,vcn_sort]) 
df_same = df_same[df_same.groupby('country').country.transform(len) > 1] 
df_same = df_same.drop_duplicates('country', keep = "last") 
df_same_sort = df_same[['country', 'people_fully_vaccinated']] 
df_same_sort = df_same_sort.rename(columns={'country' : 'country_vaccinations'}) 
df_same_sort.reset_index(drop=True, inplace=True) 
wp_clean = pd.concat([wp, df_same])
wp_clean = wp_clean[wp_clean.groupby('country').country.transform(len) > 1]
wp_clean = wp_clean.drop_duplicates('country', keep = "first")
wp_clean_sort = wp_clean[['country', '2021_last_updated']]
wp_clean_sort = wp_clean_sort.sort_values('country')
wp_clean_sort.reset_index(drop = True, inplace=True)
cbn = pd.concat([wp_clean_sort, df_same_sort], axis=1)

cbn = cbn.dropna()
cbn = cbn.reset_index()

cbn.replace(',','', regex=True, inplace=True)
cbn['2021_last_updated'] = cbn['2021_last_updated'].map(lambda x: float(x))
cbn['people_fully_vaccinated'] = cbn['people_fully_vaccinated'].map(lambda x: float(x))




#1 People who are fully vaccinated in all the Countries

people_fully_vaccined = df.groupby(['country'])['people_fully_vaccinated'].count(
).reset_index().rename(columns={'people_fully_vaccinated': 'vaccinated'})

colors = ['aqua', ] * 219
colors[171] = 'red'

fig = px.bar(data_frame=people_fully_vaccined, x=people_fully_vaccined.country,
             y=people_fully_vaccined.vaccinated, labels=dict(x="country", y="Count"),)
fig.update_layout(title="Number of people fully vaccinated",
                  titlefont={'size': 26}, template='simple_white'
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=1, opacity=1, marker_color=colors)

st.plotly_chart(fig, use_container_width=True)

st.markdown('From the above graph, it shows the Scotland as the highest in the world with total number of people fully vaccinated.')



st.markdown('---')
#2 10 Highest Countries with Vaccination
total = df.groupby('country', as_index=False).max().reset_index()
fhc = total.sort_values('total_vaccinations', ascending=False).head(10)


st.subheader('Top 10 Countries With Highest Vaccinations Progress')
# st.dataframe(fhc)
fig = px.bar(fhc, 
             x='country', 
             y='total_vaccinations',
             labels = {'country' : 'Country', 'total_vaccinations' : 'Total Vaccinations'}
            )
st.plotly_chart(fig, use_container_width=True)

st.markdown('From the above graph, it shows the China as the number one in the world with total number of vaccinations done.')


st.markdown('---')
#3 10 Lowest Countries with Vaccination
flc = total.sort_values('total_vaccinations', ascending=False).tail(10)

fig = px.bar(flc, 
             x='country', 
             y='total_vaccinations',
             labels = {'country' : 'Country', 'total_vaccinations' : 'Total Vaccinations'},
             title = "Top 10 Countries With Lowest Vaccinations Progress"
            )
st.plotly_chart(fig, use_container_width=True)

st.markdown('From the above graph, it shows the Pitcairn as the lowest in the world with total number of vaccinations done.')


st.markdown("---")
#4 Find the global average total vaccinations by month
df['date'] = pd.to_datetime(df['date'])
avg = df[df['country'] == selCon].groupby(df['date'].dt.strftime('%B'))['daily_vaccinations'].mean().sort_values().reset_index()

vg = avg.reindex([0, 1, 2, 3, 4, 5, 7, 6, 8])

fig = px.line(avg, 
             x='date', 
             y='daily_vaccinations',
             labels = {'daily_vaccinations' : 'Global Monthly Vaccinations', 'date' : 'Month'},
             title = "Average Total Vaccinations"
            )
st.plotly_chart(fig, use_container_width=True)
st.markdown('From the above graph, it shows the average total vaccinations from all over world of all the months and ')

st.markdown('---')
#5 Vaccines Occupancy
vpc = vbm[df['country'] == selCon].groupby(['vaccine', 'location'])['total_vaccinations'].max().reset_index()
vr = vpc.groupby('vaccine')['total_vaccinations'].sum().reset_index()
vr = vr.sort_values('total_vaccinations', ascending=False)

fig = px.pie(vr, values='total_vaccinations', names='vaccine', title='Vaccines Occupancy' )
st.plotly_chart(fig, use_container_width=True)


st.markdown('---')
#6 Overview of Vaccines
fig = px.bar(vr, 
             y='total_vaccinations', 
             x='vaccine',
             labels = {'vaccine' : 'Vaccines', 'total_vaccinations' : 'Total Vaccinations'},
             title = "Overview of Vaccines"
            )
st.plotly_chart(fig, use_container_width=True)


st.markdown('---')
#7 Scatterplot
pvt = pd.pivot_table(data = vbm, index = ['location'], columns = ['vaccine'], values = 'total_vaccinations', aggfunc = 'max')
pvt.fillna(0)
pd.reset_option('display.float_format') # Re-format to get float values
pd.set_option('display.float_format', lambda x: '%.2f' % x) # Set number of figure after doc
cbn['percentage'] = ((cbn['people_fully_vaccinated'])/(cbn['2021_last_updated']))*100 # Set percentage value under % type
cbn = cbn.drop(index = [61])
cbn['percentage'] = ((cbn['people_fully_vaccinated'])/(cbn['2021_last_updated']))*100 # Set percentage value under % type
tfh = cbn.sort_values('percentage', ascending=False).head(5)
cbn.sort_values('percentage').head(5)

fig = px.scatter(cbn[df['country'] == selCon], 
                y="2021_last_updated", 
                x="percentage",
                labels = {'2021_last_updated' : 'Population', 'percentage' : 'Percentage'},
                title = "Scatterplot"
               )
st.plotly_chart(fig, use_container_width=True)


st.markdown('---')
#8 Scatterplot excluding outliers
pd.set_option('display.float_format', lambda x: '%.0f'% x)
cbn = cbn.sort_values('2021_last_updated', ascending=False)
qt1 = cbn['2021_last_updated'].quantile(0.25) # Quantile 1
qt3 = cbn['2021_last_updated'].quantile(0.75) # Quantile 3
IQR_cbn = qt3 - qt1 # Quantile range
Upper_cbn = qt3 + 1.5*IQR_cbn # Upper whisker
Lower_cbn = qt1 - 1.5*IQR_cbn # Lower whisker 
cbn_sort = cbn[(Lower_cbn < cbn['2021_last_updated']) & (cbn['2021_last_updated'] < Upper_cbn)].reset_index()

fig = px.scatter(cbn_sort, 
                y="2021_last_updated", 
                x="percentage",
                labels = {'2021_last_updated' : 'Population', 'percentage' : 'Percentage'},
                title = "Scatterplot excluding outliers"
               )
st.plotly_chart(fig, use_container_width=True)