import streamlit as st
import os
import plotly.express as px
import numpy as np
import pandas as pd
# Create a list of options

## Filename of the sales
filename_sales = "./data/Product Sales_Candidate Attach 1_PresSE_013.csv"
filename_dayparts  = "./data/Dayparts_Candidate Attach 3_PresSE_013.csv"
filename_weather = "./data/Weather_Candidate Attach 4_PresSE_013.csv"
filename_demography = "./data/Demographics_Candidate Attach 2_PresSE_013.csv"
df_weather = pd.read_csv(filename_weather)


df_sales = pd.read_csv(filename_sales)
df_dayparts =pd.read_csv(filename_dayparts)

df_sales_dayparts =df_sales.merge(df_dayparts, on = ['REST_KEY','Reporting Day', 'Rest Coop'], how = 'inner')

df_demography = pd.read_csv(filename_demography, skiprows=[0])

df_agg = df_sales_dayparts.groupby(['REST_KEY', 'Reporting Day'])['Daypart Sales $'].sum()
df_sales_agg =df_agg.reset_index()

print(df_sales_agg.head())
options = list(df_sales_agg['REST_KEY'].unique())

st.sidebar.title("Resturant Insights")
selected_option = st.sidebar.selectbox('Resturant ID', options)
st.write("Resturant ID : ", selected_option)
# Create a dropdown list
# selected_option = st.selectbox('Resturant ID', options)


df_sales_agg['Reporting Day']=pd.to_datetime(df_sales_agg['Reporting Day'])
df_sales_agg = df_sales_agg.sort_values(by = 'Reporting Day', ascending = True)
if selected_option :
    temp = df_sales_agg[df_sales_agg['REST_KEY']==selected_option]
    mean_temp = temp['Daypart Sales $'].mean()
    fig = px.line(temp,x = 'Reporting Day', y ='Daypart Sales $', title = 'REST_KEY vs SALES in USD')

    ##adding mean line
    fig.update_layout(shapes=[
        dict(
        type= 'line',
        yref= 'y', y0= mean_temp, y1= mean_temp,   # adding a horizontal line at Y = 1
        xref= 'paper', x0= 0, x1= len(temp['Reporting Day']),
        line=dict(color='yellow', width=2, dash='dash')
            )
        ])
st.markdown(''' The yellow is the mean line of the sale of a particular Resturant ''')
    # fig.add_annotation(
    #                     x=len(temp['Reporting Day'])-1, y=mean_temp,
    #                     text=f"Mean: {mean_temp:.2f}",
    #                     xref="x", yref="y",
    #                     showarrow=True,
    #                     font=dict(color='yellow')
    #                 )


    # fig.add_shape(
    #                 type='line',
    #                 x0=0, x1=len(temp)-1,
    #                 y0=mean_temp, y1=mean_temp,
    #                 yref='y',
    #                 line=dict(color='red', width=2, dash='dash')
    #         )

# Display the selected option
st.plotly_chart(fig)

fig_group = px.line(df_sales_agg,x = 'Reporting Day', y ='Daypart Sales $', color = 'REST_KEY', title= 'Resturant Sales Comparison')
st.plotly_chart(fig_group)

df_sales_dayparts['REST_KEY'] = "R"+"_"+df_sales_dayparts['REST_KEY'].astype('str')
fig_box_plot_sales_dayparts = px.box(df_sales_dayparts, x ='REST_KEY', y = 'Daypart Sales $', color='REST_KEY', title = 'Distribution of Sales in Resturant')
st.plotly_chart(fig_box_plot_sales_dayparts)

### Aggerate sales of all resturant

agg_sales_by_resturant = df_sales_agg.groupby('REST_KEY').sum()
agg_sales_by_resturant = agg_sales_by_resturant.reset_index()



fig_pie_chart = px.pie(agg_sales_by_resturant, values = 'Daypart Sales $',names = 'REST_KEY'
                       ,title = 'Total Sales in USD for all resturant')
st.plotly_chart(fig_pie_chart)

agg_sales_daypart =df_sales_dayparts.groupby(['REST_KEY', 'Daypart Name'])['Daypart Sales $'].sum()

agg_sales_daypart = agg_sales_daypart.reset_index()
agg_sales_daypart['REST_KEY'] = "R"+"_"+agg_sales_daypart['REST_KEY'].astype('str')
print(agg_sales_daypart.head())
fig_agg_sales_daypart = px.histogram(agg_sales_daypart, x="REST_KEY", y="Daypart Sales $",
             color='Daypart Name', barmode='group', text_auto = True,
             height=400, title = "Total sales in USD for all day along with all resturant")

st.plotly_chart(fig_agg_sales_daypart)

st.write('Heatmap for Sales and Dayparts')
temp_sales_dayparts=df_sales_dayparts[['Daypart Sales $','POS Consumer Price',
       'POS Total Units Sold  Promo and Regular', 'POS Promotion Units Sold',
       'POS Units Sold', 'POS Combo Units Sold', 'Daypart Name',
       'Daypart Description',  'Daypart Transaction Qty']]
fig_sales_heatmap_daypart = px.imshow(temp_sales_dayparts.corr(), color_continuous_scale=r'portland')
st.plotly_chart(fig_sales_heatmap_daypart)

total_meal_count = df_sales.groupby(['REST_KEY'])[['POS Total Units Sold  Promo and Regular','POS Combo Units Sold']].sum()
total_meal_count = total_meal_count.reset_index()
total_meal_count['REST_KEY'] = "R"+"_"+total_meal_count['REST_KEY'].astype('str')

fig_total_meal_count  = px.bar(total_meal_count, x='REST_KEY', y='POS Total Units Sold  Promo and Regular', color = 'POS Total Units Sold  Promo and Regular',title = 'Total POS Unit sold Promo and Regular')
st.plotly_chart(fig_total_meal_count)


fig_total_meal_count_combo  = px.bar(total_meal_count, x='REST_KEY', y='POS Combo Units Sold', color = 'POS Combo Units Sold',title = 'Total Combo Unit sold')
st.plotly_chart(fig_total_meal_count_combo)


demography_household_count =df_demography[['REST_KEY','HOUSEHLDSC']]
demography_household_count['REST_KEY'] ="R"+"_"+demography_household_count['REST_KEY'].astype('str')

fig_pie_chart_household = px.bar(demography_household_count, x = 'REST_KEY',y  = 'HOUSEHLDSC', color = 'HOUSEHLDSC', title = 'Household Count'
                       )
st.plotly_chart(fig_pie_chart_household)
st.text('''we can see only one resturant area has urban population and it is counting to
        most of the sales even it household count is less''')
st.write(df_demography[['REST_KEY','Soc-U1','Soc-U2']])


df_weather['TY_DATE']=pd.to_datetime(df_weather['TY_DATE'])
df_weather.rename(columns= {'GEO_NAME':'Rest Coop'}, inplace = True)
df_sales_agg['Rest Coop'] = 'SEA/TCA WA CP-0024'
df_sales_weather =df_sales_agg.merge(df_weather, on = ['Rest Coop'], how = 'inner')
df_sales_weather =df_sales_weather.select_dtypes(include=[np.number, 'datetime'])
col_weather_drop = ['Unnamed: 6','GEO_CODE']
df_sales_weather = df_sales_weather.drop(columns=col_weather_drop)
col_to_include = ['Daypart Sales $', 'TY_DATE', 'TY_MODEL',
       'TY_NON_WX_MODEL', 'TY_SIG_TEMP_NEG_PCT', 'TY_SIG_TEMP_POS_PCT',
       'TY_SIG_RAIN_PCT', 'TY_SIG_SNOW_PCT', 'TY_SIG_SNOW_AND_RAIN_PCT',
       'TY_NULL_FORECAST', 'TY_MISSING_TEMP', 'TY_MISSING_PRECIP', 'LY_MODEL',
       'LY_NON_WX_MODEL', 'LY_SIG_TEMP_NEG_PCT', 'LY_SIG_TEMP_POS_PCT',
       'LY_SIG_RAIN_PCT', 'LY_SIG_SNOW_PCT', 'LY_SIG_SNOW_AND_RAIN_PCT',
       'LY_NULL_FORECAST', 'LY_MISSING_TEMP', 'LY_MISSING_PRECIP',
       'TY_AVG_MIN_TEMP', 'TY_AVG_MAX_TEMP', 'TY_TOTAL_PRECIP',
       'TY_TOTAL_SNOW', 'LY_AVG_MIN_TEMP', 'LY_AVG_MAX_TEMP',
       'LY_TOTAL_PRECIP', 'LY_TOTAL_SNOW', 'NRM_AVG_MIN_TEMP',
       'NRM_AVG_MAX_TEMP', 'NRM_TOTAL_PRECIP', 'NRM_TOTAL_SNOW', 'tytrn',
       'lytrn', 'comp', 'tybase', 'lybase', 'monthyr', 'tychg', 'lychg',
       'impactty', 'impactly', 'tycompwoweather', 'compduetoweather']
df_sales_weather_with_spec_col = df_sales_weather[col_to_include]
df_sales_weather_with_spec_col = df_sales_weather_with_spec_col.dropna(axis=1, how='any')
fig_sales_heatmap_weather = px.imshow(df_sales_weather_with_spec_col.corr(), color_continuous_scale='bluered')

# Show the plot
st.plotly_chart(fig_sales_heatmap_weather)
print(df_sales_weather.columns)

def f_to_c(f):
    c = (f-32)*(5/9)
    return c

df_weather['tempeature_celcius_avg_min'] = df_weather['TY_AVG_MIN_TEMP'].apply(lambda x: f_to_c(x))
df_weather['tempeature_celcius_avg_max'] = df_weather['TY_AVG_MAX_TEMP'].apply(lambda x: f_to_c(x))
fig_temp = px.line(df_weather, x = 'TY_DATE', y ='tempeature_celcius_avg_max', title = 'Average Max Temperature Plot')
st.plotly_chart(fig_temp)

fig_temp_min = px.line(df_weather, x = 'TY_DATE', y = 'tempeature_celcius_avg_min', title = 'Average Min Temperature Plot')
st.plotly_chart(fig_temp_min)

df_demography['REST_KEY'] = df_demography['REST_KEY'].astype('int')
df_sales_demography = df_dayparts.merge(df_demography, on = ['REST_KEY'], how='inner')
for_heat_map_sales_demography = df_sales_demography[['Daypart Sales $', 'Daypart Transaction Qty',

       'afr_amr_cons', 'hisp_cons', 'asian_cons', 'HOUSEHLDSC', 'Soc-U1',
       'Soc-U2', 'Soc-U3', 'Soc-S1', 'Soc-S2', 'Soc-S3', 'Soc-S4', 'Soc-C1',
       'Soc-C2', 'Soc-C3', 'Soc-T1', 'Soc-T2', 'Soc-T3', 'Soc-T4', 'Life-Y1',
       'Life-Y2', 'Life-Y3', 'Life-F1', 'Life-F2', 'Life-F3', 'Life-F4',
       'Life-M1', 'Life-M2', 'Life-M3', 'Life-M4', 'Prom Soc', 'Prom Life',
       'Row', 'PNECY_URB', 'PNECY_SUB', 'PNECY_CITY', 'PNECY_TR']]


fig_sales_heatmap_demography = px.imshow(for_heat_map_sales_demography.corr(), color_continuous_scale='portland', title = 'DayPart and Sales Heat Map')
st.plotly_chart(fig_sales_heatmap_demography)
