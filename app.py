import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import base64




st.markdown('*<p>Hey There! <br> Welcome To My Project. </p>*',unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4c0787;'>📈COVID-19 Vaccination Dashboard💉</h1>", unsafe_allow_html=True)
st.markdown("<p style=' font-size: 18px;'>Tracking the global vaccination progress against COVID-19</p>", unsafe_allow_html=True)
st.image('covid.jpg', use_container_width=True)

st.markdown("## 🌍 Project Overview")

st.markdown("""Welcome to the **COVID-19 Vaccination Analysis Dashboard**!  
This interactive web application visualizes global vaccination progress using real-world data sourced from [Kaggle](https://www.kaggle.com/). The goal is to provide insights into how different countries have progressed with their vaccination campaigns over time.

### 🔍 What This Dashboard Offers:

- 📊 **Total Vaccinations**: Compare the top and bottom 10 countries by total vaccinations.
- 🌎 **Global Trends**: Explore the average daily vaccinations month-wise.
- 💉 **Vaccine Usage**: See which vaccines are most widely used around the world.
- 📈 **Population vs. Vaccination**: Understand how fully vaccinated people compare to the population in each country.
- 📌 **Dynamic Metrics**: View real-time stats with animated metrics (coming up below).
- 📍 **Country Selector**: Customize views by selecting individual countries from the sidebar.

This tool is especially useful for public health researchers, data analysts, students, and anyone interested in understanding the global COVID-19 response.

""")

st.markdown('<h1>Vaccination Dataset</h1>',unsafe_allow_html=True)
st.markdown('I found this dataset on Kaggle.')




#background

def add_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('bg2.jpg')




#sidebar

sidebar = st.sidebar
sidebar.image("author2.jpeg", caption="Anjali Chaudhary", use_container_width=True)
sidebar.markdown(" 📧 Contact: 7393851899")
sidebar.markdown("- Email: [chaudharyanjali815@gmail.com](mailto:you@example.com)")
sidebar.markdown("- GitHub: [https://github.com/anjali-chaudhary11](https://github.com/anjali-chaudhary11)")


sidebar.markdown("---")


sidebar.title('Covid-19 Vaccination Data Visualization')

df=pd.read_csv ('country_vaccinations.csv')
vbm=pd.read_csv('country_vaccinations_by_manufacturer.csv')
wp=pd.read_csv('2021_population.csv')
st.dataframe(df)
countries = df.country.unique()
selCon = sidebar.selectbox(label="Select Country", options=countries)
sidebar.checkbox('Confirm')
sidebar.button("Submit")

st.markdown('---')

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

people_fully_vaccined = df.groupby('country')['people_fully_vaccinated'].max().reset_index().rename(columns={'people_fully_vaccinated': 'vaccinated'})

colors = ['aqua', ] * len(people_fully_vaccined)

max_index = people_fully_vaccined['vaccinated'].idxmax()
highlight_index = people_fully_vaccined.index.get_loc(max_index)
colors[highlight_index] = 'red'

fig = px.bar(data_frame=people_fully_vaccined, x=people_fully_vaccined.country,
             y=people_fully_vaccined.vaccinated, labels=dict(x="country", y="vaccinated"),)
fig.update_layout(
        title={
            'text': "Number of People fully Vaccinated",
            'font': {'size': 26}
        },
        template='simple_white'
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=1, opacity=1, marker_color=colors)

st.plotly_chart(fig, use_container_width=True)

st.markdown('From the above graph, it shows the China as the highest in the world with total number of people fully vaccinated.')

st.markdown('---')




#2 10 Highest Countries with Vaccination

total = df.groupby('country', as_index=False).max().reset_index()
fhc = total.sort_values('total_vaccinations', ascending=False).head(10)


# st.dataframe(fhc)
fig = px.bar(fhc, 
             x='country', 
             y='total_vaccinations',
             labels = {'country' : 'Country', 'total_vaccinations' : 'Total Vaccinations'},
             title = "Top 10 Countries With Highest Vaccinations Progress"
            )
st.plotly_chart(fig, use_container_width=True)

st.markdown('From the above graph, it shows the China as the number one in the world with maximum number of vaccinations done.')

st.markdown('---')




#3 10 Lowest Countries with Vaccination

flc = total.sort_values('total_vaccinations', ascending=True).head(10)

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


avg['date'] = pd.to_datetime(avg['date'], format='%B')
avg = avg.sort_values('date')
avg['date'] = avg['date'].dt.strftime('%B')


fig = px.line(avg, 
             x='date', 
             y='daily_vaccinations',
             labels = {'daily_vaccinations' : 'Global Monthly Vaccinations', 'date' : 'Month'},
             title = "Average Total Vaccinations"
            )
st.plotly_chart(fig, use_container_width=True)
st.markdown('From the above graph, it shows the average total vaccinations from all over world of all the months.')

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

st.markdown('---')




#9 People fully vaccinated per Country

import plotly.express as px

map_data = df.dropna(subset=['iso_code', 'people_fully_vaccinated'])
latest_map = map_data.sort_values('date').drop_duplicates('country', keep='last')

fig = px.choropleth(
    latest_map,
    locations='iso_code',
    color='people_fully_vaccinated',
    hover_name='country',
    color_continuous_scale='Viridis',
    title='🌍 People Fully Vaccinated per Country'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')




st.markdown("## 🧾 Conclusion")

st.markdown("""The analysis highlights the global effort in combating the COVID-19 pandemic through vaccination. By examining the total number of fully vaccinated individuals, vaccine manufacturers, and vaccination coverage compared to population size, we gain valuable insights into public health infrastructure, global disparities, and overall vaccine uptake.

### ✨ Key Takeaways:
- 🌟 Countries like **China**, **India**, and the **USA** lead in total vaccinations.
- 🧬 Vaccines such as **Pfizer/BioNTech**, **Moderna**, and **AstraZeneca** are widely used globally.
- 📉 Some smaller or less-developed nations still lag behind in total vaccinations.
- 📈 Data visualization empowers clearer understanding of progress, patterns, and outliers.

This project is a testament to how data science and visualization can help make complex global health data more accessible and informative. Let’s continue to spread awareness and encourage informed public health decisions.""")


st.markdown("""
    <hr style="border:1px solid #f0f0f0;">
    <p style='text-align: center; color: gray;'>
        Made with ❤️ by Anjali | Data Source: Kaggle & OWID
    </p>
""", unsafe_allow_html=True)
