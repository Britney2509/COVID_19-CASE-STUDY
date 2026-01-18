#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#LOADING DATASET


# In[58]:


import pandas as pd
import datetime

path = r"C:\Users\kisho\OneDrive\Desktop\case_study_covid.xlsx"

covid_deaths = pd.read_excel(path, sheet_name = 'covid_19_deaths_v1')
covid_deaths


# In[5]:


confirmed_cases = pd.read_excel(path, sheet_name = 'covid_19_confirmed_v1')
confirmed_cases


# In[6]:


recovered = pd.read_excel(path, sheet_name = 'covid_19_recovered_v1')
recovered


# In[ ]:


#melt:
#pd.melt(frame,id_vars=None,value_vars=None,var_name=None,value_name="value",col_level=None,ignore_index=True)


# In[16]:


#id_vars
id_vars = covid_deaths.iloc[:,0:4].columns.tolist()


# In[18]:


#value_vars
date_col = covid_deaths.iloc[:,4:].columns.tolist()


# In[19]:


deaths_long = pd.melt(covid_deaths,id_vars,value_vars=date_col,var_name='Date',value_name='Death')
deaths_long


# In[23]:


#confirmed_cases - MELT

all_cols = confirmed_cases.columns.tolist()
#print(all_cols)
id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long']

date_cols = [c for c in all_cols if c not in id_vars]
#print(date_cols)
confirmed_long = pd.melt(confirmed_cases,id_vars,value_vars=date_cols, var_name = 'Date',value_name='Confirmed')
confirmed_long


# In[54]:


#recovered

all_cols = recovered.columns.tolist()

id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long']

date_cols = [c for c in all_cols if c not in id_vars]
#print(date_cols)
recovered_long = pd.melt(recovered,id_vars,value_vars=date_cols, var_name = 'Date',value_name='Recovered')
recovered_long


# In[31]:


#CLEANING DATASET


# In[29]:


deaths_long['Province/State'].value_counts(dropna = False)


# In[30]:


deaths_long.info()


# In[ ]:


-----------------------------------------------------------------------------------------------------------------------------------


# In[33]:


deaths_long['Province/State'] = deaths_long['Province/State'].fillna('All Provisions')
deaths_long['Lat'] = deaths_long['Lat'].fillna(0)
deaths_long['Long'] = deaths_long['Long'].fillna(0)
deaths_long['Date'] = pd.to_datetime(deaths_long['Date'], format = "%m/%d/%y",errors='coerce')

deaths_long.info()


# In[ ]:


---------------------------------------------------------------------------------------------------------------------------------#


# In[34]:


confirmed_long.info()


# In[41]:


confirmed_long['Province/State'].value_counts(dropna=False)


# In[42]:


confirmed_long['Province/State'] = confirmed_long['Province/State'].fillna('All Provisions')
confirmed_long['Lat'] = confirmed_long['Lat'].fillna(0)
confirmed_long['Long'] = confirmed_long['Long'].fillna(0)
confirmed_long['Date'] = pd.to_datetime(confirmed_long['Date'], format = "%m/%d/%y",errors='coerce')

confirmed_long.info()


# In[ ]:


----------------------------------------------------------------------------------------------------------------


# In[43]:


recovered_long['Province/State'].value_counts(dropna=False)


# In[57]:


recovered_long['Province/State'] = recovered_long['Province/State'].fillna('All Provisions')
recovered_long['Lat'] = recovered_long['Lat'].fillna(0)
recovered_long['Long'] = recovered_long['Long'].fillna(0)
recovered_long['Date'] = pd.to_datetime(recovered_long['Date'], format = "%m/%d/%y",errors='coerce')

recovered_long.info()


# In[ ]:


# GROUPING AND AGGREGATION


# In[48]:


deaths_grouped = deaths_long.groupby(['Country/Region','Date'])['Death'].sum().reset_index()
deaths_grouped


# In[49]:


confirmed_grouped = confirmed_long.groupby(['Country/Region','Date'])['Confirmed'].sum().reset_index()
confirmed_grouped


# In[59]:


recovered_grouped = recovered_long.groupby(['Country/Region','Date'])['Recovered'].sum().reset_index()
recovered_grouped


# In[62]:


merged_data = (deaths_grouped
               .merge(confirmed_grouped, on = ['Country/Region','Date'], how = 'inner')
               .merge(recovered_grouped, on = ['Country/Region','Date'], how = 'inner')
            .sort_values(['Country/Region','Date']))
merged_data


# In[ ]:


# Confirmed cases over time for top countries


# In[65]:


confirmed_grouped.groupby('Country/Region')['Date'].max().reset_index()

# we get the same date'2021-12-05' as the max date


# In[71]:


top_5 = confirmed_grouped[confirmed_grouped['Date'] == '2021-12-05'].nlargest(5, 'Confirmed')
top_5


# In[69]:


#alternative approach (if the dates are different)
#here we get the same output bcoz of the same date '2021-12-05'

confirmed_grouped.loc[confirmed_grouped.groupby('Country/Region')['Date'].idxmax()].nlargest(5, 'Confirmed')


# In[74]:


country_list = top_5['Country/Region'].tolist()
country_list


# In[76]:


# Visualization for top 5 countries over time (confirmed)
import matplotlib.pyplot as plt
plt.figure(figsize=(14,5))
for country in country_list:
    top_countries = confirmed_grouped[confirmed_grouped['Country/Region']==country].sort_values('Date')
    plt.plot(top_countries['Date'],top_countries['Confirmed'],label = country)
plt.title('Total Confirmed cases over time for top 5 countries')
plt.xlabel('Date')
plt.ylabel('Cummulative Confirmed Cases')
plt.legend()
plt.show()


# In[78]:


#china
plt.figure(figsize=(14,5))
top_countries = confirmed_grouped[confirmed_grouped['Country/Region']== 'China'].sort_values('Date')
plt.plot(top_countries['Date'],top_countries['Confirmed'],label = 'China')
plt.title('Total Confirmed cases over time in China')
plt.xlabel('Date')
plt.ylabel('Cummulative Confirmed Cases')
plt.legend()
plt.show()


# In[82]:


# 
china_df = confirmed_long[confirmed_long['Country/Region']== 'China'].sort_values('Confirmed', ascending = False)
china_df


# In[96]:


china_wide = china_df.pivot_table(index = 'Date',values = 'Confirmed',columns = 'Province/State')
china_wide


# In[97]:


china_province = china_wide.iloc[-1].nlargest(5)
china_province


# In[98]:


china_wide=china_wide[china_province.index]
china_wide


# In[103]:


import matplotlib.pyplot as plt
ax = china_wide.plot(figsize=(14,6))
ax.set_title("Top 5 provinces in China with confirmed cases")
ax.set_xlabel("Date")
ax.set_ylabel("Confirmed cases")
ax.legend(china_province.index)
plt.show()


# In[106]:


# Daily new cases in Germany, France, Italy
target_countries = ['France', 'Germany', 'Italy']


# In[110]:


confirmed_cases = confirmed_grouped[confirmed_grouped['Country/Region'].isin(target_countries)]
confirmed_cases


# In[117]:


#confirmed_cases['lag']=confirmed_cases.groupby('Country/Region')['Confirmed'].shift(1).fillna(0)
#confirmed_cases


# In[118]:


#confirmed_cases['Daily cases'] = confirmed_cases['Confirmed'] - confirmed_cases['lag'] 
#confirmed_cases


# In[119]:


# alternative approch
confirmed_cases['Daily cases'] = confirmed_cases.groupby('Country/Region')['Confirmed'].diff().fillna(0)
confirmed_cases


# In[126]:


daily_cases_pivot = confirmed_cases.pivot(values = 'Daily cases', index = 'Date', columns = 'Country/Region').sort_index()
daily_cases_pivot


# In[127]:


daily_new_country_dict = {}
for country in target_countries:
    if country in daily_cases_pivot:
        series = daily_cases_pivot[country]
        daily_new_country_dict[country] = series
daily_new_country_dict


# In[129]:


peaks = {}
for country,series in daily_new_country_dict.items():
    max_value = int(series.max())
    max_index = series.idxmax().date().strftime("%y-%m-%d")
    peaks[country] = (max_value,max_index)
peaks


# In[130]:


import matplotlib.pyplot as pd
plt.figure(figsize=(14,5))
for country,series in daily_new_country_dict.items():
    plt.plot(series.index, series.values, label = country)

plt.title("Daily cases in targeted countries")
plt.xlabel('Date')
plt.ylabel('Daily cases')
plt.legend()
plt.show()


# In[141]:


# Recovered/Confirmed -- Canada and Australia -- dec 31,2020
# Which country has better management of pandamic?

country = ['Canada', 'Australia']
target_date = '2020-12-31'

recovery_data = merged_data[(merged_data['Country/Region'].isin(country)) & (merged_data['Date'] == target_date)]

recovery_data['Recovery rate'] = (recovery_data['Recovered']/recovery_data['Confirmed']*100).round(2)
recovery_data


# In[153]:


plt.figure(figsize=(11,6))
bars = plt.bar(recovery_data['Country/Region'], recovery_data['Recovery rate'],color = ['#4169E1' , '#00BFFF'])
plt.title("Recovery rate of Canada and Australia")
plt.xlabel("Country")
plt.ylabel("Recovery rate in %")
plt.bar_label(bars, fmt = '%.2f%%')
plt.show()


# In[ ]:




