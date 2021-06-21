#!/usr/bin/env python
# coding: utf-8

# # Web Scraping and Cleaning Covid-19 Datasets for Visualization, Analysis, and Geomapping

# ---
# Covid-19 is a disease caused by SARS-CoV-2.  The World Health Organization declared the disease a pandemic on March 11th, 2020. Since then there have been numerous outlets that have compiled data and presented information pertaining to its spread. Information from Worldometer, a reference website reputed by the American Library Association, will be used as the primary dataset. Worldometer gathers and compiles information from various sources, including government communication channels as well as local media. It provides live updates on the total cases, new cases, total deaths, new deaths,recoveries and critical cases by country, territory or conveyance pertaining to Covid-19. 
# 
# ---

# ### Overview:
# 
# This project will provide a broad level overview of the Covid-19 pandemic. It will contain information scraped from the most recent update on the Worldometer website. Other datasets will be used in order to supplement the information from the Worldometer dataset. Steps will be explained for data wrangling using Pandas in order to make data ready for visualization using MatPlotLib and Seaborn, correlation analysis using StatsModel Summary, and geomapping using Plotly Express.    

# ### Steps in Analysis:
# 
# 1. Import required libraries
# 
# 2. Gather data
#     - Webscraping with BeautifulSoup and Selenium
#     - Reading in CSV files
#     - Saving information into Pandas dataframes
# 
# 3. Clean data
#     - Manage null and missing values
#     - Drop unwanted rows and columns
#     - Rename columns and observations
#     - Format datatypes
#     - Add columns with calculations
#     - Concatenate dataframes
# 
# 4. Visualization
#     - Seaborn | MatPlotLib | Plotly
#     - Pearson Correlation Heatmaps
#     - Bar Plots 
#     - Pair Plots
#     - Pie Plots
#     - Bubble Plots
# 
# 5. Linear Regression in Statsmodel Summary
# 
# 6. Global GDP Exploration
#     - Scatter Plots
#     - Pearson Correlation 
# 
# 7. GeoMapping
#     - Plotly Library
#     - Choropleth 
#     - ScatterGeo 
# 

# ### Data Sources:
# 
# - Worldometer Covid-19 Live Information (Countries and US States) 
# - GDP per Capita (Countries)
# - Geospatial Data (Countries and US States)
# - Land Size (Countries)
# 
# 

# ___________________________________________________________________________________________________________
# # Import Libraries
# 
# ----

# In[1]:


# Data Gathering
import requests                                                 # HTTP requests
import requests, io                                             # Process I/O data
import urllib.request                                           # Open URL
from bs4 import BeautifulSoup                                   # Webscraping
import pandas as pd                                             # Pandas Dataframes
import re                                                       # Regular Expressions (regex)
from numpy import inf                                           # Numpy Infinite Values
import json                                                     # Parse JSON from strings and false into Python Dictionary
import js2xml                                                   # Parse Javascript into XML
import time                                                     # Time access and conversions
from selenium import webdriver                                  # Automated web browing and scraping                          
from selenium.webdriver.firefox.options import Options          # Headless browsing
from selenium.webdriver import firefox
from webdriverdownloader import GeckoDriverDownloader
from webdriver_manager.firefox import GeckoDriverManager
import dataframe_image as dfi
import aiohttp      
from pandas.plotting import table

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Visualization
import seaborn as sns                                           # Visualization based on Matplotlib
import matplotlib as mpl                                        # Visualization for Python
from matplotlib import pyplot as plt                            # MATLAB style plotting 
get_ipython().run_line_magic('matplotlib', 'inline')
from scipy import stats                                         # Statistical functions
from scipy.stats import norm                                    # Normal Continuous random variable                          
import plotly.express as px                                     # Interactive Visualization
from plotly.subplots import make_subplots                       # Subplots for Plotly
import plotly.graph_objects as go                               # Plotly Traces

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Statistical Analysis
import numpy as np                                              # Numerical data array processing
import statsmodels.formula.api as smf                           # Statistical testing
import statsmodels.api as sm                                    # Used for Correlation Analysis

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# GeoData
import os, sys                                                  # Use operating system functionality
import geopandas as gpd                                         # Geospatial data processing
from numpy import int64                                         # Process int64
from geopandas import GeoDataFrame                              # Process Geodataframes
import geopy                                                    # Python Geocoding tool that gets coordinates
from geopy.geocoders import Nominatim                           # OpenStreetMap API

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Interactive Plots to HTML5
# import plotly.offline as py                                     # Use plotly standalone HTML saved locally
# from plotly.offline import plot                                 # Use plotly in browser
# py.init_notebook_mode()                                         # Initialize notebook mode for HTML

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Exceptions
import warnings                                                 
warnings.simplefilter(action='ignore', category=FutureWarning)  # Ignore future deprecation warnings

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Confirm Libraries Import
print('Libraries Imported Successfully.')


# ---
# # Data Gathering
# 
# ---
# 
# 

# ## WORLD DATA
# 
# ---
# 
# Beautiful Soup library will be used to scrape the table from the Worldometer website. This table will then be stored into a Pandas dataframe called `global_data`. It will contain information about each country's Covid-19 cases. This dataframe will then be concatenated with a GDP dataframe called `country_gdp`, and a land size dataframe called `country_area`, later used to calculate population density

# In[2]:


# Importing table with BeatifulSoup
url = 'https://www.worldometers.info/coronavirus/'  # Assign url
requests.get(url)
page = requests.get(url).text                       # Store request into page

# Use lxml parser to store nested html structure into Beautiful Soup object
soup = BeautifulSoup(page, 'lxml')  

# Find table using html tags
table_data = soup.find('table', id = 'main_table_countries_today')  

headers = []                                
for i in table_data.find_all('th'):         # This loop will iterate through table and find all table header
    title = i.text                          # tags <th> then save table header text into title variable
    headers.append(title)                   # to be appended into headers array

# Create columns from headers strings
raw_data = pd.DataFrame(columns = headers)  

for j in table_data.find_all('tr')[1:]:     # This loop will iterate through table rows <tr> starting from row 1.
        row_data = j.find_all('td')         # Each <td> element will be stored inside row data
        row = [tr.text for tr in row_data]  # Each element will then be stored in row variable as objects
        length = len(raw_data)
        raw_data.loc[length] = row

# Get updated date and time string
a= soup.findAll('div',attrs={"style":"font-size:13px; color:#999; margin-top:5px; text-align:center"})

last_update = (a[0].string)
print(last_update)

# Save imported data table to 'global_data' dataframe
global_data = raw_data

# Strip preceding empty spaces in columns and replace spaces with underscore
global_data.columns= global_data.columns.to_series().apply(lambda x: x.strip())
global_data.columns = (global_data.columns.str.strip().str.upper().str.replace(' ', '_'))

dfi.export(global_data, 'images/globaldataraw.png', max_rows=10)
global_data.head()


# ### GDP Per Capita
# 
# ---
# 
# This dataset will be used to see if GDP per capita has any influence in the amount of Covid-19 cases per country, the death rate, survival rate, etc. Each country's GDP per capita will be contained in the dataframe, which will then be added to the `global_data` dataframe.

# In[3]:


# Read in csv and save to 'country_gdp' dataframe
country_gdp = pd.read_csv("Resources\csvGDP.csv")

dfi.export(country_gdp, 'images/countrygdpraw.png', max_rows=10)
country_gdp.head()


# ### Land Area (MI<sup>2</sup>)
# 
# ---
# 
# Land area dataset will be used to calculate the population density. Population density will be used to see if there is correlation with total cases, death rate, survival rate, etc. Each country's land size will be contained in the dataframe, which will then be added to the `global_data` dataframe

# In[4]:


# Import table with BeatifulSoup
url3 = 'https://www.worldometers.info/geography/largest-countries-in-the-world/'
requests.get(url3)
page3 = requests.get(url3).text

soup3 = BeautifulSoup(page3, 'lxml')

table_data3 = soup3.find('table', id = 'example2')

headers = []
for i in table_data3.find_all('th'):
    title = i.text
    headers.append(title)

raw_data3 = pd.DataFrame(columns = headers)

for j in table_data3.find_all('tr')[1:]:
         row_data = j.find_all('td')
         row = [tr.text for tr in row_data]
         length = len(raw_data3)
         raw_data3.loc[length] = row

# Save imported data table to 'country_area' dataframe
country_area = raw_data3

# Strip preceding empty spaces in columns and replace spaces with underscore
country_area.columns= country_area.columns.to_series().apply(lambda x: x.strip())
country_area.columns = (country_area.columns.str.strip().str.upper().str.replace(' ', '_'))

dfi.export(country_area, 'images/countryarearaw.png', max_rows=10)
country_area.head()


# ## UNITED STATES DATA
# 
# ---
# 
# Using the same scraping method previously outlined, this data will primarily be used in visualization and geomapping. It will be placed into a dataframe called `us_data` and concatenated with `state_gdp`, which, will include information about each state's GDP per capita.

# In[5]:


# Import table with BeatifulSoup
url2 = 'https://www.worldometers.info/coronavirus/country/us/'
requests.get(url2)
page2 = requests.get(url2).text

soup2 = BeautifulSoup(page2, 'lxml')

table_data2 = soup2.find('table', id = 'usa_table_countries_today')

headers = []
for i in table_data2.find_all('th')[0:13]:   # Specify only columns 0 to 12 be appended
    title = i.text
    headers.append(title)

raw_data2 = pd.DataFrame(columns = headers)

for j in table_data2.find_all('tr')[1:]:
         row_data = j.find_all('td')[:13]    # Specify only columns 0 to 12 
         row = [tr.text for tr in row_data]
         length = len(raw_data2)
         raw_data2.loc[length] = row

# Save imported data table to 'us_data' dataframe
us_data = raw_data2

# Strip preceding empty spaces in columns and replace spaces with underscore
us_data.columns= us_data.columns.to_series().apply(lambda x: x.strip())
us_data.columns = (us_data.columns.str.strip().str.upper().str.replace(' ', '_'))

dfi.export(us_data, 'images/usdataraw.png', max_rows=10)
us_data.head()


# -------
# # Data Cleaning
# 
# -----------------
# 
# Data cleaning is the process of detecting and correcting (or removing) corrupt or inaccurate records from a record set, table, or database and refers to identifying incomplete, incorrect, inaccurate or irrelevant parts of the data and then replacing, modifying, or deleting the dirty or coarse data. It is necessary for data to be consistent and organized for it to be represented accurately later on during visualization and modeling.
# 
# 
# 
# 

# **Covered in this section:**
# 
# - Dealing with null values
# - Formatting text and datatypes
# - Adding, removing, and renaming columns
# - Renaming string variables contained in rows
# - Editing CSV data

# ## WORLD DATA
# 
# ---
# 
# This dataset has inconsistencies in the form of newline characters, special characters, unnecessary columns and rows, and mislabeled country names.  Null values, datatypes, and column names must be formatted before merging `global_data` with `country_gdp` and `country_area`. Several values are missing from the `country_gdp` dataset; after merging with the `global_data` dataframe, a dataframe containing `COUNTRY` and `GDP_PER_CAPITA` variables will be exported to csv, filled in manually, and added back into the dataframe.

# In[6]:


# Format data
global_data=global_data.replace('\n','', regex=True)            # Remove newline characters (regex denotes regular expression) 
global_data=global_data.replace(',','', regex=True)             # Remove commas
global_data.columns=global_data.columns.str.replace('\n','')    # Remove newline characters from columns
global_data = global_data.applymap(lambda x: x.strip('+'))      # 'applymap' applies lambda function to remove '+' from every element in DataFrame

# Drop top buttom unwanted rows
global_data= global_data.drop(global_data.index[[0,1,2,3,4,5,6,7]]).reset_index(drop=True) # Index will be out of order, reset index

# Drop tail unwanted rows
global_data.drop(global_data.tail(8).index,inplace=True) 
global_data.head()


# In[7]:


# Rename 'global_data' columns
global_data.rename(columns={global_data.columns[10]: 'TOTCASES_PER_1M'}, inplace= True)    # Rename column using index number
global_data = global_data.rename(columns={'SERIOUS,CRITICAL': 'SERIOUS_CRITICAL',          # Rename columns using column names
                                          'COUNTRY,OTHER': 'COUNTRY', 
                                          'DEATHS/1M_POP': 'DEATH_PER_1M', 
                                          'TESTS/1M_POP': 'TESTS_PER_1M'})                      

# Drop 'global_data' columns that will not be used in analysis
global_data = global_data.drop(['#','1_CASEEVERY_X_PPL', '1_DEATHEVERY_X_PPL',
       '1_TESTEVERY_X_PPL', 'NEWCASES', 'NEWDEATHS', 'NEWRECOVERED', 'NEW_CASES/1M_POP', 'NEW_DEATHS/1M_POP', 'ACTIVE_CASES/1M_POP'], axis=1)

global_data.columns    # Lists column names


# In[8]:


# Check datatypes of 'global_data' dataframe
global_data.dtypes


# In[9]:


# Convert global_data dataframe objects to strings
global_data = global_data.astype('string')
global_data.dtypes


# In[10]:


# Rename row information to keep consistent with 'country_gdp' dataframe
global_data.COUNTRY= global_data.COUNTRY.replace("USA","United States")
global_data.COUNTRY= global_data.COUNTRY.replace("UK","United Kingdom")


# In[11]:


global_data.head()


# In[12]:


# Choose columns that will be converted to numeric
cols = ['TOTALCASES', 'TOTALDEATHS','TOTALRECOVERED', 'ACTIVECASES', 'SERIOUS_CRITICAL',
       'TOTCASES_PER_1M', 'DEATH_PER_1M', 'TOTALTESTS', 'TESTS_PER_1M',
       'POPULATION']

# Change global_data datatypes to numeric variables      
global_data[cols] = global_data[cols].apply(pd.to_numeric, errors='coerce', axis=1)

# Convert NAN and INF values to 0
global_data.fillna(0, inplace=True)
global_data.replace(np.nan, 0, inplace=True)
global_data.replace(np.inf, 0, inplace=True)

# Convert columns 1 to 10 to int
for col in global_data.columns[1:11]: 
    global_data[col]=global_data[col].apply(int)

global_data.dtypes


# In[13]:


# China's is out of order, so we have to sort TOTALCASES
global_data = global_data.sort_values(['TOTALCASES'], ascending= False)

dfi.export(global_data, 'images/globaldataclean.png', max_rows=10)
global_data.head()


# ### Country GDP Per Capita
# 
# ---

# In[14]:


# Rename 'country_gdp' columns to be consistent with 'global_data' columns for later concatenation
country_gdp = country_gdp.rename(columns = {'country': 'COUNTRY', 
                                            'gdpPerCapita': 'GDP_PER_CAPITA'})

# Drop 'country_gdp' unnecessary columns 
country_gdp = country_gdp.drop(['rank','imfGDP', 'unGDP', 'pop'], axis=1)

country_gdp.columns     # Lists column names


# In[15]:


# Check country_gdp datatype
country_gdp.dtypes


# In[16]:


# Convert 'COUNTRY' variable from 'object' to 'string'
country_gdp['COUNTRY'] = country_gdp['COUNTRY'].astype('string')

dfi.export(country_gdp, 'images/countrygdpclean.png', max_rows=10)
country_gdp.dtypes


# ### Country Land Area
# 
# ---

# In[17]:


# Remove newline characters
country_area=country_area.replace('\n','', regex=True)
country_area=country_area.replace(',','', regex=True)
country_area=country_area.replace('square miles','', regex=True)

# Drop and Rename Columns
country_area = country_area.drop(['#', 'TOT._AREA_(KM²)', 'TOT._AREA_(MI²)', '%_OF_WORLD_LANDMASS', 'LAND_AREA_(KM²)'], axis=1)
country_area = country_area.rename(columns={'LAND_AREA_(MI²)': 'LAND_AREA'})

# Convert country_area dataframe objects to strings and numeric
country_area = country_area.astype('string')
country_area['LAND_AREA'] = country_area['LAND_AREA'].apply(pd.to_numeric)
country_area.head()


# In[18]:


# Rename rows to keep consistent with 'country_gdp' dataframe to successfully merge dataframes
country_area.COUNTRY= country_area.COUNTRY.replace("United Arab Emirates","UAE")
country_area.COUNTRY= country_area.COUNTRY.replace("State of Palestine","Palestine")
country_area.COUNTRY= country_area.COUNTRY.replace("Republic of North Macedonia","North Macedonia")
country_area.COUNTRY= country_area.COUNTRY.replace("South Korea","S. Korea")
country_area.COUNTRY= country_area.COUNTRY.replace("Côte d'Ivoire","Ivory Coast")
country_area.COUNTRY= country_area.COUNTRY.replace("DR Congo","DRC")
country_area.COUNTRY= country_area.COUNTRY.replace("China Hong Kong SAR","Hong Kong")
country_area.COUNTRY= country_area.COUNTRY.replace("Central African Republic","CAR")
country_area.COUNTRY= country_area.COUNTRY.replace("Turks and Caicos Islands","Turks and Caicos")
country_area.COUNTRY= country_area.COUNTRY.replace("Saint Vincent and the Grenadines","St. Vincent Grenadines")
country_area.COUNTRY= country_area.COUNTRY.replace("Saint Barthélemy","St. Barth")
country_area.COUNTRY= country_area.COUNTRY.replace("Brunei Darussalam","Brunei")
country_area.COUNTRY= country_area.COUNTRY.replace("Wallis and Futuna Islands","Wallis and Futuna")
country_area.COUNTRY= country_area.COUNTRY.replace("China Macao SAR","Macao")
country_area.COUNTRY= country_area.COUNTRY.replace("Holy See","Vatican City")
country_area.COUNTRY= country_area.COUNTRY.replace("Saint Pierre and Miquelon","Saint Pierre Miquelon")

dfi.export(country_area, 'images/countryareaclean.png', max_rows=10)


# ### Concatenation
# 
# ---
# 
# The `global_data` dataframe is ready to be concatenated with the `country_gdp` dataframe.  A left merge will be used in order to add the `'GDP_PER_CAPITA'` variable to the existing `global_data` dataframe. Merging on `'COUNTRY'` will allow each dataframe to use the `'COUNTRY'` column as its index to match each row from `global_data` to `country_gdp` based on the country's name. This explains why each country's name in both datasets had to be exact. Any country name that is not identical in both dataframes will not merge, returning an NAN value in the `'GDP_PER_CAPITA'` column. `country_area` will be merged the same way.

# In[19]:


# Merge datasets
global_data = global_data.merge(country_gdp, on='COUNTRY', how='left')
global_data.head()


# Calculations will be made in order to add a `'DEATH_RATE'`, `'SURVIVAL_RATE'`, and `'PERCENT_TESTS_POSITIVE'` column to the `global_data` dataframe

# In[20]:


# Death Rate = Total Deaths / Total Cases
global_data['DEATH_RATE'] = global_data.TOTALDEATHS / global_data.TOTALCASES

# Survival Rate = Total Recovered / Total Cases
global_data['SURVIVAL_RATE'] = global_data.TOTALRECOVERED / global_data.TOTALCASES

# Percentage of Tests Positive = Total Cases / Total Tests
global_data['PERCENT_TESTS_POSITIVE'] = global_data.TOTALCASES / global_data.TOTALTESTS
global_data = global_data.replace([np.inf, -np.inf], 0)     # If numerator is '0', infinite number (inf) will be added. Replace it with '0'
global_data.head()


# ### Null values
# 
# ---
# 
# The `country_gdp` dataframe was missing GDP per capita values for several countries before it was added to `global_data`. These need to be added manually. First, a new dataframe will be created, `gdp_entry`, which will only contain the `'COUNTRY'` and `'GDP_PER_CAPITA'`columns from `global_data` using a `copy()` function.  This dataframe will then be exported to a csv file called `gdp_entry.csv`. Once the GDP values are manually added to the csv, it will be saved as `gdp_entry2.csv` and read into a dataframe called `gdp_df_update`. The `GDP_PER_CAPITA` column must first be dropped from `global_data` before merging the `gdp_df_update` dataframe. The rows `Diamond Princess` and `MS Zaandam` will be dropped because they are ships, but first `'COUNTRY'` must be set as the index in order to drop the rows by axis 0. After that, the index is reset.

# In[21]:


# Check for NAN values
global_data[global_data.isna().any(axis=1)]


# In[22]:


# Create dataframe to have NAN values filled in manually
gdp_entry = global_data[['COUNTRY', 'GDP_PER_CAPITA']].copy()
gdp_entry.head()


# In[23]:


#Export dataframe to csv in order to manually add GDP information
gdp_entry.to_csv('Resources\gdp_entry.csv', index = False)


# In[24]:


# Add updated csv to dataframe
gdp_df_update= pd.read_csv('Resources\gdp_entry2.csv')

# Drop current country_gdp column
global_data= global_data.drop('GDP_PER_CAPITA', axis=1)

# Merge updated gdp dataframe back into 'global_data'
global_data = global_data.merge(gdp_df_update, on='COUNTRY', how='left')

# Drop the rows that are ships and not countries
global_data = global_data.set_index('COUNTRY')                                              # Set index to 'COUNTRY' to delete rows on axis 0
global_data = global_data.drop(['Diamond Princess','MS Zaandam'], axis = 0).reset_index()   # Rows must be deleted using name because they may change index
global_data.head()                                                                          # based on TOTALCASES count on Worldometer


# In[25]:


# Merge 'country_area' with 'global_data' 
# Strip will be used on the 'COUNTRY' column in order remove any missed spaces before or after string
global_data.COUNTRY = global_data.COUNTRY.str.strip()
country_area.COUNTRY = country_area.COUNTRY.str.strip()
global_data = global_data.merge(country_area, on='COUNTRY', how='left')


# In[26]:


# Percentage of Tests Positive
global_data['POPULATION_DENSITY'] = global_data.POPULATION / global_data.LAND_AREA


# In[160]:


# Check dataframe for null values
globalisnull = global_data.isnull().any()


#create a subplot without frame
plot = plt.subplot(111, frame_on=False)

#remove axis
plot.xaxis.set_visible(False) 
plot.yaxis.set_visible(False) 

#create the table plot and position it in the upper left corner
table(plot, globalisnull, loc='upper left')

#save the plot as a png file
plt.savefig('images/globalisnull.png', bbox_inches = "tight")


# In[28]:


dfi.export(global_data, 'images/globaldataconcat.png', max_rows=10)
global_data.head()


# ## UNITED STATES DATA
# 
# ---
# 
# This dataset has inconsistencies in the form of newline characters, special characters, and unnecessary columns and rows. Datatypes and column names will be formatted before merging `us_data` with `state_gdp`. Woldometer does not have `ACTIVECASES` and `TOTALRECOVERED` data for Hawaii and South Carolina available in the tabe; this information will be retrieved from each state's URL.

# In[29]:


#remove newline characters and special characters in dataframe
us_data=us_data.replace('\n','', regex=True)
us_data=us_data.replace(',','', regex=True)
us_data.columns=us_data.columns.str.replace('\n','')
us_data = us_data.applymap(lambda x: x.strip('+'))
us_data.head()


# 

# In[30]:


#Drop top unwanted rows and reset index
us_data= us_data.drop(us_data.index[[0]]).reset_index(drop=True)

#drop tail unwanted rows
us_data.drop(us_data.tail(13).index,inplace=True)
us_data.head()


# In[31]:


# Rename columns
us_data.rename(columns = {us_data.columns[8]: 'TOTCASES_PER_1M'}, inplace = True)

us_data = us_data.rename(columns = {'USASTATE':'STATE', 
                                    'DEATHS/1M_POP': 'DEATH_PER_1M', 
                                    'TOT CASES/1M_POP' : 'TOTCASES_PER_1M', 
                                    'TESTS/1M_POP': 'TESTS_PER_1M'})

# Drop unwanted columns
us_data = us_data.drop(['#', 'NEWCASES', 'NEWDEATHS'], axis = 1)
us_data.columns


# In[32]:


# Convert global_data dataframe objects to strings
us_data = us_data.astype('string')
us_data.dtypes


# In[33]:


# Change us_data datatypes to numeric
cols = ['TOTALCASES', 'TOTALDEATHS','TOTALRECOVERED', 'ACTIVECASES',
       'TOTCASES_PER_1M', 'DEATH_PER_1M', 'TOTALTESTS', 'TESTS_PER_1M',
       'POPULATION']
       
us_data[cols] = us_data[cols].apply(pd.to_numeric, errors='coerce', axis=1)

# Convert columns to integer
for col in us_data.columns[1:]: 
    us_data[col]=pd.Series(us_data[col], dtype=int)

us_data.dtypes


# In[34]:


# ADD COLUMNS

# Death Rate per Country
us_data['DEATH_RATE'] = us_data.TOTALDEATHS / us_data.TOTALCASES

# Survival Rate
us_data['SURVIVAL_RATE'] = us_data.TOTALRECOVERED / us_data.TOTALCASES

# Percentage of Tests Positive
us_data['PERCENT_TESTS_POSITIVE'] = us_data.TOTALCASES / us_data.TOTALTESTS

#us_data = us_data.replace([np.inf, -np.inf], 0)
us_data.head()


# ### Null Values
# 
# ---
# 
# In order to get the most accurate visualization, null values must be taken care of. Some visualization libraries will not process cells that have <NA> values, so those must be coverted to NaN. In this dataset, NaN values can still be found an added to the dataframe using webscraping. 

# In[35]:


us_data[us_data.isna().any(axis =1)]


# The above states are are missing values in three columns. They will be added using BeautifulSoup from their individual state pages.

# ### Get Hawaii Recovered Cases
# 
# ---
# 
# The number of recovered cases can be found directly on the state's page in the `span` tag. It will be parsed using an lxml interpreter and stored in a soup variable. The variable `a` will store the elements of the `class: "maincounter-number"` tag, and then `find` will be used on `a` to find the contents of the `span` tag. This process will be replicated for South Carolina. District of Columbia's GDP Per Capita will be found manually and added to the dataframe

# In[36]:


url4 = 'https://www.worldometers.info/coronavirus/usa/hawaii/'
requests.get(url4)
page4 = requests.get(url4).text

soup4 = BeautifulSoup(page4, 'lxml')
# Get updated date and time string
a= soup4.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

hawaii_recovered = a.find('span').text
hawaii_recovered = hawaii_recovered.replace(",", "")
hawaii_recovered = int(hawaii_recovered)
print(hawaii_recovered)


# ### Get Hawaii Active Cases
# 
# ---
# 
# The information for Hawaii's active cases is stored in an interactive table on the state's website. `Selenium` will be used in order to browse the page using a Firefox webdriver. The elements of the JavaScript `Highchart.chart tag` will be stored in the variable `temp`. The data array will store all elements of `series`, which contains the number of active cases over time. The most recently updated value for Hawaii's active cases will be used. This process will be replicated for South Carolina.

# In[37]:


website = "https://www.worldometers.info/coronavirus/usa/hawaii/"

option = Options()
option.headless = True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
data = [item for item in temp]
hawaii_active = (data[-1])
print(hawaii_active)
driver.quit()


# ### Get South Carolina Recovered Cases
# 
# ---

# In[38]:


url5 = 'https://www.worldometers.info/coronavirus/usa/south-carolina/'
requests.get(url5)
page5 = requests.get(url5).text
soup5 = BeautifulSoup(page5, 'lxml')
# Get updated date and time string
a= soup5.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

scarolina_recovered = a.find('span').text
scarolina_recovered = scarolina_recovered.replace(",", "")
scarolina_recovered = int(scarolina_recovered)
print(scarolina_recovered)


# ### Get South Carolina Active Cases
# 
# ---

# In[39]:


website = "https://www.worldometers.info/coronavirus/usa/south-carolina/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
scarolina_active = (data[-1])
scarolina_active = int(scarolina_active)
print(scarolina_active)
driver.quit()


# ### Get Indiana Recovered Cases
# 
# ---

# In[40]:


url6 = 'https://www.worldometers.info/coronavirus/usa/indiana/'
requests.get(url6)
page6 = requests.get(url6).text
soup6 = BeautifulSoup(page6, 'lxml')
# Get updated date and time string
a= soup6.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

indiana_recovered = a.find('span').text
indiana_recovered = indiana_recovered.replace(",", "")
indiana_recovered = int(indiana_recovered)
print(indiana_recovered)


# ### Get Indiana Active Cases
# 
# ---

# In[41]:


website = "https://www.worldometers.info/coronavirus/usa/indiana/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
indiana_active = (data[-1])
indiana_active = int(indiana_active)
print(indiana_active)
driver.quit()


# ### Get Wisconsin Recovered
# 
# ---

# In[42]:


url7 = 'https://www.worldometers.info/coronavirus/usa/wisconsin/'
requests.get(url7)
page7 = requests.get(url7).text
soup7 = BeautifulSoup(page7, 'lxml')
# Get updated date and time string
a= soup7.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

wisconsin_recovered = a.find('span').text
wisconsin_recovered = wisconsin_recovered.replace(",", "")
wisconsin_recovered = int(wisconsin_recovered)
print(wisconsin_recovered)


# ### Get Wisconsin Active
# 
# ---

# In[43]:


website = "https://www.worldometers.info/coronavirus/usa/wisconsin/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
wisconsin_active = (data[-1])
wisconsin_active = int(wisconsin_active)
print(wisconsin_active)
driver.quit()


# alabamarecovered

# In[44]:


url8 = 'https://www.worldometers.info/coronavirus/usa/alabama/'
requests.get(url8)
page8 = requests.get(url8).text
soup8 = BeautifulSoup(page8, 'lxml')
# Get updated date and time string
a= soup8.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

alabama_recovered = a.find('span').text
alabama_recovered = alabama_recovered.replace(",", "")
alabama_recovered = int(alabama_recovered)
print(alabama_recovered)


# alabama acive

# In[45]:


website = "https://www.worldometers.info/coronavirus/usa/alabama/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
alabama_active = (data[-1])
alabama_active = int(alabama_active)
print(alabama_active)
driver.quit()


# lousiana rec

# In[46]:


url9 = 'https://www.worldometers.info/coronavirus/usa/louisiana/'
requests.get(url9)
page9 = requests.get(url9).text
soup9 = BeautifulSoup(page9, 'lxml')
# Get updated date and time string
a= soup9.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

louisiana_recovered = a.find('span').text
louisiana_recovered = louisiana_recovered.replace(",", "")
louisiana_recovered = int(louisiana_recovered)
print(louisiana_recovered)


# louisiana active

# In[47]:


website = "https://www.worldometers.info/coronavirus/usa/louisiana/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
louisiana_active = (data[-1])
louisiana_active = int(louisiana_active)
print(louisiana_active)
driver.quit()


# nebraska rec

# In[48]:


url10 = 'https://www.worldometers.info/coronavirus/usa/nebraska/'
requests.get(url10)
page10 = requests.get(url10).text
soup10 = BeautifulSoup(page10, 'lxml')
# Get updated date and time string
a= soup10.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

nebraska_recovered = a.find('span').text
nebraska_recovered = nebraska_recovered.replace(",", "")
nebraska_recovered = int(nebraska_recovered)
print(nebraska_recovered)


# nebraska active

# In[49]:


website = "https://www.worldometers.info/coronavirus/usa/nebraska/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
nebraska_active = (data[-1])
nebraska_active = int(nebraska_active)
print(nebraska_active)
driver.quit()


# maine recovered

# In[50]:


url11 = 'https://www.worldometers.info/coronavirus/usa/maine/'
requests.get(url11)
page11 = requests.get(url11).text
soup11 = BeautifulSoup(page11, 'lxml')
# Get updated date and time string
a= soup11.find('div',attrs={"class": "maincounter-number", "style": "color:#8ACA2B "})

maine_recovered = a.find('span').text
maine_recovered = maine_recovered.replace(",", "")
maine_recovered = int(maine_recovered)
print(maine_recovered)


# maine active

# In[51]:


website = "https://www.worldometers.info/coronavirus/usa/maine/"

option = Options()
option.headless= True
driver = webdriver.Firefox(options= option)
driver.get(website)
time.sleep(5)

temp = driver.execute_script('return window.Highcharts.charts[3]'
                             '.series[0].options.data')
                             
data = [item for item in temp]
maine_active = (data[-1])
maine_active = int(maine_active)
print(maine_active)
driver.quit()


# In[52]:


us_data.STATE = us_data.STATE.str.strip()


# In[53]:


us_data=us_data.set_index('STATE')


# ### REPLACE VALUES FOR HAWAII AND SOUTH CAROLINA

# In[54]:


us_data.at['Hawaii','TOTALRECOVERED'] = hawaii_recovered                                                                   # Locate cell and replace with value
us_data.at['Hawaii','ACTIVECASES'] = hawaii_active                                                                                 
us_data.at['Hawaii','SURVIVAL_RATE'] = (hawaii_recovered / (us_data.at['Hawaii', 'TOTALCASES']))                          # Replace with calculation

us_data.at['South Carolina','TOTALRECOVERED'] = scarolina_recovered
us_data.at['South Carolina','ACTIVECASES'] = scarolina_active
us_data.at['South Carolina','SURVIVAL_RATE'] = (scarolina_recovered / (us_data.at['South Carolina', 'TOTALCASES']))

us_data.at['Indiana','TOTALRECOVERED'] = indiana_recovered
us_data.at['Indiana','ACTIVECASES'] = indiana_active
us_data.at['Indiana','SURVIVAL_RATE'] = (indiana_recovered / (us_data.at['Indiana', 'TOTALCASES']))

us_data.at['Wisconsin','TOTALRECOVERED'] = wisconsin_recovered
us_data.at['Wisconsin','ACTIVECASES'] = wisconsin_active
us_data.at['Wisconsin','SURVIVAL_RATE'] = (wisconsin_recovered / (us_data.at['Wisconsin', 'TOTALCASES']))

us_data.at['Alabama','TOTALRECOVERED'] = alabama_recovered
us_data.at['Alabama','ACTIVECASES'] = alabama_active
us_data.at['Alabama','SURVIVAL_RATE'] = (alabama_recovered / (us_data.at['Alabama', 'TOTALCASES']))

us_data.at['Louisiana','TOTALRECOVERED'] = louisiana_recovered
us_data.at['Louisiana','ACTIVECASES'] = louisiana_active
us_data.at['Louisiana','SURVIVAL_RATE'] = (louisiana_recovered / (us_data.at['Louisiana', 'TOTALCASES']))

us_data.at['Nebraska','TOTALRECOVERED'] = nebraska_recovered
us_data.at['Nebraska','ACTIVECASES'] = nebraska_active
us_data.at['Nebraska','SURVIVAL_RATE'] = (nebraska_recovered / (us_data.at['Nebraska', 'TOTALCASES']))

us_data.at['Maine','TOTALRECOVERED'] = maine_recovered
us_data.at['Maine','ACTIVECASES'] = maine_active
us_data.at['Maine','SURVIVAL_RATE'] = (maine_recovered / (us_data.at['Maine', 'TOTALCASES']))


# In[159]:


# DataFrame cleaned of all null values
usdataisnull = us_data.isnull().any()
usdataisnull

#create a subplot without frame
plot = plt.subplot(111, frame_on=False)

#remove axis
plot.xaxis.set_visible(False) 
plot.yaxis.set_visible(False) 

#create the table plot and position it in the upper left corner
table(plot, usdataisnull,loc='upper left')

#save the plot as a png file
plt.savefig('images/usdataisnull.png', bbox_inches = "tight")


# In[56]:


# Reset index
us_data = us_data.reset_index()

dfi.export(us_data, 'images/usdataclean.png', max_rows=10)
us_data.tail()


# # Visualization
# 
# --------------
# </br>
# 
# **Covered in this section:** 
# - Bar chart subplots using Seaborn and MatPlotLib
# - Interactive Pie chart subplots using Plotly Express
# - Pearson Correlation Heatmap using Seaborn
# 

# ## Top Countries
# 
# ---

# In[57]:


# Create dataframe of the top ten countries with the most confirmed cases
top_cases = global_data[:10] 
top_cases.head()


# ### Bar Subplot
# 
# ---
# 
# A barplot shows the relationship between a numeric and a categoric variable. Each entity of the categoric variable is represented as a bar. The size of the bar represents its numeric value. A barplot is used to aggregate the categorical data according to some methods and by default it’s the mean. It can also be understood as a visualization of the group by action. To use this plot we choose a categorical column for the x-axis and a numerical column for the y-axis, and we see that it creates a plot taking a mean per categorical column.
# 
# A barplot will be used to plot the top cases.  Because there are fewer X variables, the variation between the bar bars will be easier to visualize
# 

# In[58]:


# Use Seaborn and Matplotlib to create bar subplot for all variable in 'topcases' dataframe

fig, ax = plt.subplots(8, 2, figsize= (25,25))                                                          # Plots with 8 row, 2 column dimension for subplots

ax1 = sns.barplot(top_cases["COUNTRY"], top_cases["TOTALCASES"], data= top_cases, ax = ax[0,0])         # Subplot with 'COUNTRY' x variable, 'TOTALCASES' y variable
ax1.set_title("Total Cases", fontsize=15)

ax2 = sns.barplot(top_cases["COUNTRY"], top_cases["TOTALDEATHS"], data= top_cases, ax = ax[0,1])
ax2.set_title("Total Deaths", fontsize=15)

ax3 = sns.barplot(top_cases["COUNTRY"], top_cases["TOTALRECOVERED"], data= top_cases, ax = ax[1,0])
ax3.set_title("Total Recovered", fontsize=15)

ax4 = sns.barplot(top_cases["COUNTRY"], top_cases["ACTIVECASES"], data= top_cases, ax = ax[1,1])
ax4.set_title("Active Cases", fontsize=15)

ax5 = sns.barplot(top_cases["COUNTRY"], top_cases["SERIOUS_CRITICAL"], data= top_cases, ax = ax[2,0])
ax5.set_title("Serious and Critical Cases", fontsize=15)

ax6 = sns.barplot(top_cases["COUNTRY"], top_cases["TOTCASES_PER_1M"], data= top_cases, ax = ax[2,1])
ax6.set_title("Total Cases Per Million", fontsize=15)

ax7 = sns.barplot(top_cases["COUNTRY"], top_cases["DEATH_PER_1M"], data= top_cases, ax = ax[3,0])
ax7.set_title("Total Deaths Per Million", fontsize=15)

ax8 = sns.barplot(top_cases["COUNTRY"], top_cases["TOTALTESTS"], data= top_cases, ax = ax[3,1])
ax8.set_title("Total Tests", fontsize=15)

ax9 = sns.barplot(top_cases["COUNTRY"], top_cases["TESTS_PER_1M"], data= top_cases, ax = ax[4,0])
ax9.set_title("Total Tests Per Million", fontsize=15)

ax10 = sns.barplot(top_cases["COUNTRY"], top_cases["POPULATION"], data= top_cases, ax = ax[4,1])
ax10.set_title("Population", fontsize=15)

ax11 = sns.barplot(top_cases["COUNTRY"], top_cases["DEATH_RATE"], data= top_cases, ax = ax[5,0])
ax11.set_title("Death Rate", fontsize=15)

ax12 = sns.barplot(top_cases["COUNTRY"], top_cases["SURVIVAL_RATE"], data= top_cases, ax = ax[5,1])
ax12.set_title("Survival Rate", fontsize=15)

ax13 = sns.barplot(top_cases["COUNTRY"], top_cases["PERCENT_TESTS_POSITIVE"], data= top_cases, ax = ax[6,0])
ax13.set_title("Percent of Tests Positive", fontsize=15)

ax14 = sns.barplot(top_cases["COUNTRY"], top_cases["GDP_PER_CAPITA"], data= top_cases, ax = ax[6,1])
ax14.set_title("GDP per Capita", fontsize=15)

ax15 = sns.barplot(top_cases["COUNTRY"], top_cases["POPULATION_DENSITY"], data= top_cases, ax= ax[7,0])
ax15.set_title("Population Density", fontsize=15)

ax16 = sns.barplot(top_cases["COUNTRY"], top_cases["POPULATION_DENSITY"], data= top_cases, ax= ax[7,1])
ax16.set_title("Population Density", fontsize=15)

# Convert y axis label from 'e' notation to plain
for ax in ax.flat:
    ax.ticklabel_format(axis='y', style = 'plain') 

# Delete empty subplot
fig.delaxes(ax = ax16)


fig.suptitle('TOP TEN COUNTRIES BAR PLOTS' + ', ' + last_update, fontsize = 30)     # Barchart title
fig.tight_layout(pad=0.6, w_pad=0.5, h_pad=3)                                       # Padding
fig.subplots_adjust(top=.92)                                                        # Space between title and plots

fig.savefig('images/toptenbarplot.png', facecolor='w')


# ### Interactive Pie Subplot
# 
# ---
# 
# The interactive pie charts will be made using `Plotly Express`. A pie chart is a circular analytical chart, which is divided into region to symbolize numerical percentage. In px.pie, data anticipated by the sectors of the pie to set the values. All sectors are classified bynames. Pie chart is used to show the percentage with the next corresponding slice of pie. Pie chart easily understandable due to its different portions and color codings.  Labels can be found by hovering over the chart.

# In[59]:


fig = make_subplots(rows=7, 
                    cols=2, 
                    specs=[[{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}], [{"type": "pie"},                                          {"type":"pie"}], [{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}]], 
                    subplot_titles=('Confirmed Cases', 'Death Rate', 'Survival Rate', 'Percent of Tests Positive', 'Total Deaths', 'Total Recovered', 'Active Cases',                                    'Serious', 'Deaths Per Million', 'Total Tests', 'Tests Per Million', 'Population', 'Population Density'), 
                    vertical_spacing=0.05,)

# Add pie charts
fig.add_trace(go.Pie(                   # Add pie plot using Plotly Graph Object
     values=top_cases.TOTALCASES,       # y variable
     labels=top_cases.COUNTRY,          # x variable
     domain=dict(x=[0, 0.5]),           # Position on Domain
     name="T_Cases"),                   # Tag
     row=1, col=1)                      # Position on Plot

fig.add_trace(go.Pie(
     values=top_cases.DEATH_RATE,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="Death Rate"),
     row=1, col=2)
     
fig.add_trace(go.Pie(
     values=top_cases.SURVIVAL_RATE,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0, 0.5]),
     name="Survival"), 
     row=2, col=1)

fig.add_trace(go.Pie(
     values=top_cases.PERCENT_TESTS_POSITIVE,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="Tests Pos"),
     row=2, col=2)

fig.add_trace(go.Pie(
     values=top_cases.TOTALDEATHS,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="T_Deaths"),
     row=3, col=1)
     
fig.add_trace(go.Pie(
     values=top_cases.TOTALRECOVERED,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0, 0.5]),
     name="T_Recovered"), 
     row=3, col=2)

fig.add_trace(go.Pie(
     values=top_cases.ACTIVECASES,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="Active"),
     row=4, col=1)

fig.add_trace(go.Pie(
     values=top_cases.SERIOUS_CRITICAL,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="Serious"),
     row=4, col=2)

fig.add_trace(go.Pie(
     values=top_cases.DEATH_PER_1M,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="DeathsPM"),
     row=5, col=1)
     
fig.add_trace(go.Pie(
     values=top_cases.TOTALTESTS,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0, 0.5]),
     name="T_Tests"), 
     row=5, col=2)

fig.add_trace(go.Pie(
     values=top_cases.TESTS_PER_1M,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0.5, 1.0]),
     name="TestsPM"),
     row=6, col=1)

fig.add_trace(go.Pie(
     values=top_cases.POPULATION,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0, 0.5]),
     name="Population"), 
     row=6, col=2)

fig.add_trace(go.Pie(
     values=top_cases.POPULATION_DENSITY,
     labels=top_cases.COUNTRY,
     domain=dict(x=[0, 0.5]),
     name="Population Density"), 
     row=7, col=1)

# Update layout
fig['layout'].update(
     height=3000, 
     width=900, 
     title='<b>Top 10 Countries</b>' + ', ' + last_update, 
     title_x= .5, 
     title_font_size = 15, 
     hovermode = "x unified")

fig.show()
fig.write_image("images/pie.png")


# ### Pearson Correlation Heatmap

# In[60]:


# Correlation Between Total Tests and Total Cases
plt.figure(figsize=(20,8))

# Numerical variables to be used in Pearson Correlation Heatmap
pc = top_cases[['TOTALCASES', 'TOTALDEATHS','TOTALRECOVERED', 'ACTIVECASES', 'SERIOUS_CRITICAL',
              'TOTCASES_PER_1M', 'DEATH_PER_1M', 'TOTALTESTS', 'TESTS_PER_1M',
              'POPULATION', 'DEATH_RATE', 'SURVIVAL_RATE', 'PERCENT_TESTS_POSITIVE', 'GDP_PER_CAPITA', 'POPULATION_DENSITY']].corr()

# Plot correlation using Seaborn
sns.heatmap(pc, 
            cmap="Blues", 
            linewidth=0.3, 
            cbar_kws={"shrink": .8}, 
            annot= True)

# Set title
plt.title(  "Top Countries Heatmap" + ', ' + last_update, size= 20, pad = 50)

plt.savefig('images/toptenheat.png', facecolor='w')


# ## World Data
# 
# ----------

# In[61]:


global_data.head()


# ### Interactive Bubble Plot
# 
# ---
# 
# The bubble chart in Plotly can be created using the `scatter()` method of plotly.express. A bubble chart is a data visualization which helps to displays multiple circles (bubbles) in a two-dimensional plot as same in scatter plot. A third dimension of the data is shown through the size of markers. A bubble chart is primarily used to depict and show relationships between numeric variables.

# In[62]:


# Grouped Dataframe with Sorted Values
global_confirmed = pd.DataFrame(global_data.groupby('CONTINENT')['TOTALCASES'].sum().sort_values(ascending = False))

fig1 = px.scatter(global_confirmed,                                                         # Create Plotly Express scatter figure
                x = global_confirmed.index,                                                 # X variable
                y = 'TOTALCASES',                                                           # Y varaible
                size = 'TOTALCASES',                                                        # Bubble size based on value counts
                size_max = 100,                                                             # Max bubble size
                color = global_confirmed.index,                                             # Hue
                title = '<b>Total Confirmed Cases by Continent</b>' + ', ' + last_update,       
                width=900, 
                height= 600)

fig1['layout'].update(title_x= .5, title_font_size = 15)                                                          # Title Position
fig1.show()

fig1.write_image('images/bubble.png')


# ### Interactive Scatter Plot
# 
# ---
# 
# These interactive scatter plot was created using Plotly Express. A scatter plot is a diagram where each value is represented by the dot graph. Scatter plot needs arrays of the same length, one for the value of x-axis and the other for the y-axis. Each data is represented as a dot point, whose location is given by x and y columns. It can be created using the `scatter()` method of `plotly.express`

# In[63]:


fig = px.scatter(global_data,                                                                                                   # Create Plotly Express scatter figure
                x="TESTS_PER_1M",                                                                                               # X variable
                y="TOTCASES_PER_1M",                                                                                            # Y variable
                color="CONTINENT",                                                                                              # Hue
                trendline= False,                                                                                               # No Trendline
                log_x = True,                                                                                                   # X axis log scale
                log_y= True,                                                                                                    # Y axis log scale
                title = '<b>Total confirmed COVID-19 cases per million vs Total tests per million</b>' + ', ' + last_update,    # Tit
                labels=dict(TESTS_PER_1M="Tests Per Million", TOTCASES_PER_1M="Total Confirmed Cases Per Million"),             # Hover labels 
                custom_data=["COUNTRY"])

fig.update_layout(  width=900, 
                    height=600, 
                    title_x= .5, 
                    showlegend= True, 
                    hovermode="x unified",
                    title_font_size = 12)

yaxis={'tickformat':'e', 'rangemode': 'tozero',     # Format Y ticks
           'ticks': 'outside'} 
xaxis={'tickformat':'e', 'rangemode': 'tozero',     # Format X ticks
           'ticks': 'outside'} 

fig.update_traces(                                  # Update fig scatter plot
        hovertemplate="<br>".join([                 # Assign labels to hover box from variables in fig
        "TESTS PER MILLION: %{x}",                  # Customize name of X data 
        "TOTAL CASES PER MILLION: %{y}",            # Customuze name of Y data
        "COUNTRY: %{customdata[0]}"                 # Assign to position 0 of custom_data
    ])
)
fig.show()

fig.write_image('images/totaltestscatter.png')


# In[64]:


fig = px.scatter(global_data, 
                x="POPULATION_DENSITY", 
                y="TOTCASES_PER_1M", 
                color="CONTINENT", 
                trendline= False, 
                log_x = True, 
                log_y= True, 
                title = '<b>Total confirmed COVID-19 cases per million vs Population Density</b>' + ', ' + last_update, 
                labels=dict(POPULATION_DENSITY="Population Density", TOTCASES_PER_1M="Total Confirmed Cases Per Million"), 
                custom_data=["COUNTRY"])

fig.update_layout(  width=900, 
                    height=600, 
                    title_x= .5, 
                    showlegend= True, 
                    hovermode="x unified",
                    title_font_size = 12)

yaxis={'tickformat':'e', 'rangemode': 'tozero',
           'ticks': 'outside'} 
xaxis={'tickformat':'e', 'rangemode': 'tozero',
           'ticks': 'outside'}

fig.update_traces(
        hovertemplate="<br>".join([
        "POPULATION DENSITY: %{x}",
        "TOTAL CASES PER MILLION: %{y}",
        "COUNTRY: %{customdata[0]}"
    ])
)

fig.show()

fig.write_image('images/popdenscatter.png')


# ### Bar Subplot

# In[65]:


fig2, axes = plt.subplots(8, 2, figsize= (25,25) )

axes1 = sns.barplot(global_data["CONTINENT"], global_data["TOTALCASES"], data= global_data, ax = axes[0,0])
axes1.set_title("Total Cases For Each Continent", fontsize=15)

axes2 = sns.barplot(global_data["CONTINENT"], global_data["TOTALDEATHS"], data= global_data, ax = axes[0,1])
axes2.set_title("Total Deaths For Each Continent", fontsize=15)

axes3 = sns.barplot(global_data["CONTINENT"], global_data["TOTALRECOVERED"], data= global_data, ax = axes[1,0])
axes3.set_title("Total Recovered For Each Continent", fontsize=15)

axes4 = sns.barplot(global_data["CONTINENT"], global_data["ACTIVECASES"], data= global_data, ax = axes[1,1])
axes4.set_title("Active Cases For Each Continent", fontsize=15)

axes5 = sns.barplot(global_data["CONTINENT"], global_data["SERIOUS_CRITICAL"], data= global_data, ax = axes[2,0])
axes5.set_title("Serious and Critical Cases For Each Continent", fontsize=15)

axes6 = sns.barplot(global_data["CONTINENT"], global_data["TOTCASES_PER_1M"], data= global_data, ax = axes[2,1])
axes6.set_title("Total Cases Per Million For Each Continent", fontsize=15)

axes7 = sns.barplot(global_data["CONTINENT"], global_data["DEATH_PER_1M"], data= global_data, ax = axes[3,0])
axes7.set_title("Total Deaths Per Million For Each Continent", fontsize=15)

axes8 = sns.barplot(global_data["CONTINENT"], global_data["TOTALTESTS"], data= global_data, ax = axes[3,1])
axes8.set_title("Total Tests For Each Continent", fontsize=15)

axes9 = sns.barplot(global_data["CONTINENT"], global_data["TESTS_PER_1M"], data= global_data, ax = axes[4,0])
axes9.set_title("Total Tests Per Million For Each Continent", fontsize=15)

axes10 = sns.barplot(global_data["CONTINENT"], global_data["POPULATION"], data= global_data, ax = axes[4,1])
axes10.set_title("Population For Each Continent", fontsize=15)

axes11 = sns.barplot(global_data["CONTINENT"], global_data["DEATH_RATE"], data= global_data, ax = axes[5,0])
axes11.set_title("Death Rate For Each Continent", fontsize=15)

axes12 = sns.barplot(global_data["CONTINENT"], global_data["SURVIVAL_RATE"], data= global_data, ax = axes[5,1])
axes12.set_title("Survival Rate For Each Continent", fontsize=15)

axes13 = sns.barplot(global_data["CONTINENT"], global_data["PERCENT_TESTS_POSITIVE"], data= global_data, ax = axes[6,0])
axes13.set_title("Percent of Tests Positive For Each Continent", fontsize=15)

axes14 = sns.barplot(global_data["CONTINENT"], global_data["GDP_PER_CAPITA"], data= global_data, ax = axes[6,1])
axes14.set_title("GDP per capita", fontsize=15)

axes15 = sns.barplot(top_cases["CONTINENT"], top_cases["POPULATION_DENSITY"], data= top_cases, ax= axes[7,0])
axes15.set_title("Population Density", fontsize=15)

axes16 = sns.barplot(top_cases["CONTINENT"], top_cases["POPULATION_DENSITY"], data= top_cases, ax= axes[7,1])
axes16.set_title("Population Density", fontsize=15)

fig2.delaxes(ax = axes16)

for axes in axes.flat:
    axes.ticklabel_format(axis='y', style = 'plain')
    axes.set_xticklabels(axes.get_xticklabels())

fig2.suptitle('CONTINENTS BAR PLOTS' + ', ' + last_update, fontsize = 30)
fig2.tight_layout(pad=0.6, w_pad=0.5, h_pad=3)
fig2.subplots_adjust(top=.92)

fig2.savefig('images/contbar.png', facecolor='w')


# In[66]:


us_data.columns


# ## US STATES
# 
# ---

# ### Pearson Correlation Heatmap

# In[67]:


#Correlation Between Total Tests and Total Cases
plt.figure(figsize=(20,8))

pc = us_data[['TOTALCASES', 'TOTALDEATHS','TOTALRECOVERED', 'ACTIVECASES',
       'TOTCASES_PER_1M', 'DEATH_PER_1M', 'TOTALTESTS', 'TESTS_PER_1M',
       'POPULATION', 'DEATH_RATE', 'SURVIVAL_RATE', 'PERCENT_TESTS_POSITIVE']].corr()

sns.heatmap(  pc, 
              cmap="Spectral",            # Color scheme
              linewidth=0.3,              # Spacing between squares       
              cbar_kws={"shrink": .8},    # Bar width
              annot= True)                # Include correlation value

plt.title("US Data Heatmap" + ', ' + last_update, size= 20, pad = 50)

plt.savefig('images/usheat.png', facecolor='w')


# ### Pair Plot
# 
# ---
# 
# Pairplot is a module of `Seaborn` library which provides a high-level interface for drawing attractive and informative statistical graphics. A pairplot provides a veiw of bivariate relationships in a dataset. The pairplot function creates a grid of Axes such that each variable in the data will by shared in the y-axis across a single row and in the x-axis across a single column. 

# In[68]:


sns_plot = sns.pairplot(us_data)
sns_plot.fig.suptitle("Global Data Pair Plot")
sns_plot.savefig('images/pair.png', facecolor='w')


# ---
# # CORRELATION ANALYSIS
# ---

# ## Pearson Correlation Feature Selection
# ---
# 
# Pearson Correlation measures the statistical relationship between two continuous variables.  It is known as the best method of measuring the association between variables of interest because it is based on the method of covariance.  It gives information about the magnitude of the association, or correlation, as well as the direction of the relationship.
# 
# </br> 
# 
# The Degree of Correlation denotes the following:
# - **Perfect:** If the value is near ± 1, then it said to be a perfect correlation: as one variable increases, the other variable tends to also increase (if positive) or decrease (if negative).</b>
# 
# - **High degree:** If the coefficient value lies between ± 0.50 and ± 1, then it is said to be a strong correlation.
# 
# - **Moderate degree:** If the value lies between ± 0.30 and ± 0.49, then it is said to be a medium correlation. 
# 
# - **Low degree:** When the value lies below ± .29, then it is said to be a small correlation.
# 
# - **No correlation:** When the value is zero. 
# 
# </br>
# 
# Using Seaborn Library, a heatmap will be constructed to provide a high-level view of the Pearson Correlation coefficients

# In[69]:


#Pearson correlation heatmap
plt.figure(figsize=(20,8))

pc = global_data[['TOTALCASES', 'TOTALDEATHS','TOTALRECOVERED', 'ACTIVECASES', 'SERIOUS_CRITICAL','TOTCASES_PER_1M', 'DEATH_PER_1M', 'TOTALTESTS', 'TESTS_PER_1M','POPULATION', 'DEATH_RATE', 'SURVIVAL_RATE', 'PERCENT_TESTS_POSITIVE', 'GDP_PER_CAPITA', 'POPULATION_DENSITY']].corr()

sns.heatmap(pc, 
            cmap="rainbow_r", 
            linewidth=0.3, 
            cbar_kws={"shrink": .8}, 
            annot= True)

plt.title("World Data Pearson Correlation Heatmap", 
            size= 20, 
            pad = 50)

plt.savefig('images/worldpearson.png', facecolor='w')


# The first question that was posed in the analysis aimed to determine whether the spread of Covid-19 is influenced by population density.  A higher population density could imply less social distancing. The heatmap shows that the dependent variable, `POPULATION_DENSITY` has a very low correlation with all other variables except for `GDP_PER_CAPITA`. Due to the low correlation, we can infer that population density is not a factor influencing Covid-19 cases.
# 
# The second question postulates that `GDP_PER_CAPITA` has an influence on `DEATH_RATE`, with a higher GDP indicating that a country has a better response in dealing with Covid-19 cases.  `GDP_PER_CAPITA` has a medium correlation with `TOTCASES_PER_1M`, `DEATH_PER_MILLION`, and `TESTS_PER_MILLION`.  A Statsmodels summary evaluation will be performed to investigate this correlation further.

# ## Linear Regression in Statsmodels
# ----
# 
# Linear regression is a statistical method for modelling relationship between a dependent variable with a given set of independent variables. Simple linear regression is an approach for predicting a response using a single feature. It is assumed that the two variables are linearly related. Hence, we try to find a linear function that predicts the response value(y) as accurately as possible as a function of the feature or independent variable(x).

# In[70]:


global_data.describe()


# The `DataFrame.describe()` method is used to view some basic statistical details like count, mean, std, min, max, and percentile (25th, 50th, and 75th percentiles) of a data frame or a series of numeric values.

# ### Statsmodels.summary()
# 
# ---
# 
# This linear regression analysis will be performed using the Ordinary Least Squares function from the `statsmodels` library. It compares the difference between individual points in the data set and the predicted best fit line to measure the amount of error produced. Least squares is a standard approach in regression analysis to approximate the solution by minimising the sum of the squares of the residuals.The `smf.ols()` function requires two inputs, the formula for producing the best fit line, and the dataset.
# 
# <u>Summary report will display the following</u>:
# 
# - **R-Squared**: Percent of variance explained by the model.
# 
# - **Adj. R-Squared**: R-Squared where additional independent variables are penalized
# 
# - **F-statistic**: Significance of fit
# 
# - **Prob (F-statistic)**: Probability of seeing F-statistic from a sample
# 
# - **Log-likelihood**: Log of the likelihood function
# 
# - **AIC**: Akaike Information Criterion, penalizes model when more independent variables are added.
# 
# - **BIC**: Bayesian Information Criterion, similar to AIC but with higher penalties
# 
# - **coef**: Estimated coefficient value
# 
# - **std err**: Standard error of the coefficient estimate
# 
# - **t**: Measure of statistical significance for coefficient
# 
# - **P>|t|**: Probability value that the coefficient is equal to 0
# 
# - **\[0.025 0.975]**: Lower and upper halves of 95% confidence interval
# 
# - **Omnibus**: Omnibus D’Angostino’s test, statistical test for skewness and kurtosis
# 
# - **Prob(Omnibus)**: Omnibus statistic as a probability
# 
# - **Skew**: Measure of data mean symmetry
# 
# - **Kurtosis**: Measure of shape of the distribution
# 
# - **Durbin-Watson**: Test for autocorrelation
# 
# - **Jarque-Bera (JB)**: Test for skewness & kurtosis
# 
# - **Prob (JB)**: Jarque-Bera statistic as a probability
# 
# - **Cond. No.**: Test for multicollinearity

# ### Total Cases per Million vs GDP
# 
# ---

# #### Total Cases Per Million Without Constant

# In[122]:


X = global_data[['GDP_PER_CAPITA']]             # Independent vars
y = global_data['TOTCASES_PER_1M']              # Dependant variable

model = sm.OLS(y,X, missing = 'drop').fit()     # Line of best fit
predictions = model.predict(X)                  # Prediction

model.summary()

plt.rc('figure', figsize=(7, 5))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig('images/output1.png')


# In[ ]:





# #### Total Cases Per Million With Constant

# In[121]:


X = global_data['GDP_PER_CAPITA']
y = global_data['TOTCASES_PER_1M']
X = sm.add_constant(X) # intercept (beta_0) added to model

model = sm.OLS(y,X, missing='drop').fit()
predictions = model.predict(X)

model.summary()

plt.rc('figure', figsize=(7, 5))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig('images/output2.png')


# In[73]:


fig =   px.scatter(global_data, 
        y="GDP_PER_CAPITA", 
        x="TOTCASES_PER_1M",  
        trendline= "ols", 
        log_x = False, 
        log_y= False, 
        title = '<b>COVID-19 Total cases per million vs GDP per capita</b>' + ', ' + last_update, 
        labels=dict(GDP_PER_CAPITA="GDP Per Capita", TOTCASES_PER_1M="Total Cases Per Million"), 
        custom_data=["COUNTRY"])

fig.update_layout(  width=900, 
                    height=600, 
                    title_x= .5, 
                    showlegend= True, 
                    hovermode="x unified",
                    title_font_size = 15)

yaxis=  {'tickformat':'e', 'rangemode': 'tozero',
        'ticks': 'outside'} 
xaxis=  {'tickformat':'e', 'rangemode': 'tozero',
        'ticks': 'outside'} 

fig.update_traces(
        hovertemplate="<br>".join([
        "GDP_PER_CAPITA: %{y}",
        "TOTCASES_PER_1M: %{x}",
        "COUNTRY: %{customdata[0]}"
    ])
)

fig.show()

fig.write_image('images/gdpscatter.png')


# ### Deaths Per Million vs GDP
# 
# ---

# #### Deaths Per Million Without Constant
# 

# In[123]:


X = global_data[['GDP_PER_CAPITA']] 
y = global_data['DEATH_PER_1M'] 

model = sm.OLS(y,X, missing='drop').fit()
predictions = model.predict(X)

model.summary()

plt.rc('figure', figsize=(7, 5))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig('images/output3.png')


# #### Deaths Per Million With Constant

# In[124]:


X = global_data[['GDP_PER_CAPITA']]
y = global_data['DEATH_PER_1M']
X = sm.add_constant(X)

model = sm.OLS(y,X, missing='drop').fit()
predictions = model.predict(X)

model.summary()

plt.rc('figure', figsize=(7, 5))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig('images/output4.png')


# In[76]:



fig =   px.scatter(global_data, 
        y="GDP_PER_CAPITA", 
        x="DEATH_PER_1M", 
        trendline= "ols", 
        log_x = False, 
        log_y= False, 
        title = '<b>Total confirmed COVID-19 deaths per million vs GDP per capita</b>' + ', ' + last_update, 
        labels=dict(GDP_PER_CAPITA="GDP Per Capita", DEATH_PER_1M="Deaths Per Million"), 
        custom_data=["COUNTRY", "CONTINENT"])

fig.update_layout(  width=900, 
                    height=600, 
                    title_x= .5, 
                    showlegend= True, 
                    hovermode="x unified",
                    title_font_size = 15)

yaxis={'tickformat':'e', 'rangemode': 'tozero',
           'ticks': 'outside'} 
xaxis={'tickformat':'e', 'rangemode': 'tozero',
           'ticks': 'outside'} 

fig.update_traces(
        hovertemplate="<br>".join([
        "GDP_PER_CAPITA: %{y}",
        "DEATH_PER_1M: %{x}",
        "COUNTRY: %{customdata[0]}"
    ])
)

fig.show()

fig.write_image('images/gdpdeathscatter.png')


# ### Tests Per Million vs GDP Per Capita
# 
# ---

# #### Tests Per Million Without Constant

# In[125]:


X = global_data[['GDP_PER_CAPITA']] #independent vars
y = global_data['TESTS_PER_1M'] #dependant variable

model = sm.OLS(y,X, missing='drop').fit()
predictions = model.predict(X)

model.summary()

plt.rc('figure', figsize=(7, 5))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig('images/output5.png')


# #### Tests Per Million With Constant

# In[126]:


X = global_data[['GDP_PER_CAPITA']] #independent vars
y = global_data['TESTS_PER_1M'] #dependant variable
X = sm.add_constant(X) # intercept (beta_0) added to model

model = sm.OLS(y,X, missing='drop').fit()
predictions = model.predict(X)

model.summary()

plt.rc('figure', figsize=(7, 5))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig('images/output6.png')


# In[79]:


fig = px.scatter(global_data, 
                y="GDP_PER_CAPITA", 
                x="TESTS_PER_1M",  
                trendline= "ols", 
                log_x = False, 
                log_y= False, 
                title = '<b>Total COVID-19 Tests administed per million vs GDP per capita</b>' + ', ' + last_update, 
                labels=dict(GDP_PER_CAPITA="GDP Per Capita", TESTS_PER_1M="Tests Per Million"), 
                custom_data=["COUNTRY", "CONTINENT"])

fig.update_layout(  width=900, 
                    height=600, 
                    title_x= .5, 
                    showlegend= True, 
                    hovermode="x unified",
                    title_font_size = 15)

yaxis={'tickformat':'e', 'rangemode': 'tozero',
           'ticks': 'outside'} 
xaxis={'tickformat':'e', 'rangemode': 'tozero',
           'ticks': 'outside'} 
           
fig.update_traces(
        hovertemplate="<br>".join([
        "GDP_PER_CAPITA: %{y}",
        "TESTS_PER_1M: %{x}",
        "COUNTRY: %{customdata[0]}"
    ])
)
fig.show()

fig.write_image('images/gdptestscatter.png')


# ----------
# # GEOMAPPING
# 
# ------
# 
# Spatial data, geospatial data, GIS data or geodata, are names for numeric data that identifies the geographical location of a physical object such as a building, a street, a town, a city, a country, etc. according to a geographic coordinate system. From the spatial data, you can find out not only the location but also the length, size, area or shape of any object. An example of a kind of spatial data that you can get are: coordinates of an object such as latitude, longitude, and elevation. Geographic Information Systems (GIS) or other specialized software applications can be used to access, visualize, manipulate and analyze geospatial data.

# ## Gather Geospatial Data
# 
# ---
# 
# The geospatial data used will consist of shapefiles. A shapefile is a simple, nontopological format for storing the geometric location and attribute information of geographic features. Geographic features in a shapefile can be represented by points, lines, or polygons. Latitude and longitute coordinates will be added to the dataframe using `Nominatim` to gather data from OpenStreetMap
# 
# 
# Geodata will be gathered from two different shapefiles. Each one contains country data that is missing in the other. The `df.update` function will be used to modify in place using non-NA values from a dataframe created from `global_data` merged with the dataframe containing the shapefiles.

# ### World Geospatial Data
# 
# ---

# In[80]:


global_data.head()


# #### Get Lat and Long Coordinates

# In[81]:


# Use Nominatim to get Longitude and Latitude
locator = Nominatim(user_agent="myGeocoder")

loc1_df=[]                                                              # Create empty array
for i in global_data.COUNTRY:                                           # Iterate through COUNTRY column 
        location = locator.geocode([i])                                 # Find location data for each country
        loc1_df.append([location.latitude, location.longitude])         # Append location and longitude as tuples in dataframe


# In[82]:


global_loc = pd.DataFrame(loc1_df, columns = ['LAT', 'LONG'])           # Create dataframe with latitude and longitude information

dfi.export(global_loc, 'images/globalloc.png', max_rows=10)
global_loc.head()


# In[83]:


global_data = global_data.join(global_loc)      # Join 'global_loc' dataframe with 'global_data'
global_data.head()


# #### Create Shapefile DataFrames

# In[84]:


# Copy relative path of .shp file
shapefile = 'Resources\\UIA_World_Countries_Boundaries-shp\World_Countries__Generalized_.shp'

# Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)

# Create dataframe to be merged later
gdf1=gdf[['COUNTRY','geometry']].copy()
gdf1.head()


# In[85]:


# Copy relative path of .shp file
shapefile = 'Resources\Longitude_Graticules_and_World_Countries_Boundaries-shp\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp'

# Read shapefile using Geopandas
gdf2 = gpd.read_file(shapefile)
gdf2= gdf2.rename(columns={'CNTRY_NAME': 'COUNTRY'})

# Create dataframe to be merged later
gdf3 = gdf2[['COUNTRY','geometry']].copy()

dfi.export(gdf3, 'images/globalshape2.png', max_rows=10)
gdf3.head()


# In[86]:


# The Country names in the 'gdf1' dataframe are inconsistent with those in 'global_data'
gdf1.COUNTRY= gdf1.COUNTRY.replace("Russian Federation","Russia")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Palestinian Territory","Palestine")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Czech Republic","Czechia")
gdf1.COUNTRY= gdf1.COUNTRY.replace("United Arab Emirates","UAE")
gdf1.COUNTRY= gdf1.COUNTRY.replace("South Korea","S. Korea")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Côte d'Ivoire","Ivory Coast")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Congo DRC","DRC")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Central African Republic","CAR")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Turks and Caicos Islands","Turks and Caicos")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Saint Vincent and the Grenadines","St. Vincent Grenadines")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Saint Barthelemy","St. Barth")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Brunei Darussalam","Brunei")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Saint Pierre and Miquelon","Saint Pierre Miquelon")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Curacao","Curaçao")
gdf1.COUNTRY= gdf1.COUNTRY.replace("Faroe Islands","Faeroe Islands")

dfi.export(gdf1, 'images/globalshape1.png', max_rows=10)


# #### Merge DataFrames

# In[87]:


# Set Country to String
gdf1['COUNTRY'] =pd.Series(gdf1['COUNTRY'], dtype= "string")
gdf2['COUNTRY'] =pd.Series(gdf2['COUNTRY'], dtype= "string")

# Strip Country columns
gdf1.COUNTRY = gdf1.COUNTRY.str.strip()
gdf3.COUNTRY = gdf3.COUNTRY.str.strip()
global_data.COUNTRY =global_data.COUNTRY.str.strip()

# Create new
geo_global_data = global_data.merge(gdf1, on='COUNTRY', how='left')
geo_global_data['COUNTRY'] =pd.Series(geo_global_data['COUNTRY'], dtype= "string")
geo_global_data2 = global_data.merge(gdf3, on='COUNTRY', how= 'left')


geo_global_data.update(geo_global_data2)

# Check datatypes
geo_global_data.dtypes


# #### Convert to GeoDataFrame

# In[88]:


# Convert 'geo_global_data' to GeoDataFrame
geo_global_data = GeoDataFrame(geo_global_data)
type(geo_global_data)


# #### Null values

# In[89]:


geo_global_data[geo_global_data.isna().any(axis=1)]


# #### Hong Kong Shapefile

# In[90]:


# Copy relative path of .shp file
shapefile = 'Resources\HK-shp\gadm36_HKG_0.shp'                       # Relative path to shapefile

# Read shapefile using Geopandas
hk_shp = gpd.read_file(shapefile)                           # Create Hong Kong dataframe
hk_shp= hk_shp.rename(columns={'NAME_0': 'COUNTRY'})        # Rename column
hk_shp.drop(['GID_0'], axis = 1, inplace= True)             # Drop column
hk_shp


# #### Carribean Netherlands Shapefile

# In[91]:


# Copy relative path of .shp file
shapefile = 'Resources\CarNetherlands-shp\BES_adm0.shp'

# Read shapefile using Geopandas
CN_shp = gpd.read_file(shapefile)
CN_shp= CN_shp.rename(columns={'NAME_0': 'COUNTRY'})
CN_shp.drop(['adm0code'], axis = 1, inplace= True)
CN_shp


# #### Channel Island Shapefile

# In[92]:


# Copy relative path of .shp file
shapefile = 'Resources\Channel-shp\cinms_py.shp'

# Read shapefile using Geopandas
ch_shp = gpd.read_file(shapefile)
ch_shp= ch_shp.rename(columns={'AREA_NAME': 'COUNTRY'})                             # Rename column
ch_shp.drop(['SANCTUARY', 'POLY_ID', 'DATUM'], axis = 1, inplace= True)             # Drop columns
ch_shp.drop([0], axis = 0, inplace = True)                                          # Drop row
ch_shp.COUNTRY= ch_shp.COUNTRY.replace("Northern Section","Channel Islands")        # Rename 
ch_shp


# #### Macao Shapefile

# In[93]:


# Macao Shapefile
# Copy relative path of .shp file
shapefile = 'Resources\Macao-shp\MAC_adm0.shp'

# Read shapefile using Geopandas
macao_shp = gpd.read_file(shapefile)
macao_shp= macao_shp.rename(columns={'NAME_ENGLI': 'COUNTRY'})
macao_shp.drop(macao_shp.iloc[:,:2], axis = 1, inplace= True)                           # Drop columns at index 0 and 1 (COUNTRY moves to index 0)
macao_shp.drop(macao_shp.iloc[:,1:-1], axis = 1, inplace= True)                         # Drop columns at index 1 to -1
macao_shp.COUNTRY= macao_shp.COUNTRY.replace("Northern Section","Channel Islands")
macao_shp


# #### Concatenate Shapefile DataFrames

# In[94]:


shp_df = pd.concat([macao_shp, ch_shp, CN_shp, hk_shp], axis=0)  # Vertically stack DataFrames


# In[95]:


shp_df['COUNTRY'] =pd.Series(shp_df['COUNTRY'], dtype= "string")                        # Convert to string
geo_global_data['COUNTRY'] =pd.Series(geo_global_data['COUNTRY'], dtype= "string")      # Convert to String
shp_df.COUNTRY = shp_df.COUNTRY.str.strip()                                             # Strip strings


# #### Update GeoDataFrame

# In[96]:


geo_global_data3= global_data.merge(shp_df, on='COUNTRY', how= 'left')      # Create new dataframe
geo_global_data.update(geo_global_data3)                                    # Update 'geo_global_data'

dfi.export(geo_global_data, 'images/geoglobaldata.png', max_rows=10)
geo_global_data.head()


# In[137]:


# DataFrame clean of all null values
geoisnull = geo_global_data.isnull().any()

#create a subplot without frame
plot = plt.subplot(111, frame_on=False)

#remove axis
plot.xaxis.set_visible(False) 
plot.yaxis.set_visible(False) 

#create the table plot and position it in the upper left corner
table(plot, geoisnull,loc='upper right')

#save the plot as a png file
plt.savefig('images/geoglobaldataisnull.png', bbox_inches = "tight")


# ### State Geospatial Data
# 
# ---

# In[98]:


us_data.head()


# #### Lat and Long Coordinates

# In[99]:


# Instantiate Nominatim
locator = Nominatim(user_agent="myGeocoder")

# Gather longitude and latitude coordinates
state_locs=[]                                                                   # Empty array
for i in us_data.STATE:                                                         # Iterate through 'STATES'        
        location = locator.geocode([i])                                         # Gather nominatim data for each state
        state_locs.append([location.latitude, location.longitude])              # Append as tuples


# In[100]:


state_locs


# In[101]:


# Create DataFrame with coordinates
state_loc = pd.DataFrame(state_locs, columns = ['LAT', 'LONG']) 
state_loc.head() 


# In[102]:


# Add coordinates to 'us_data' DataFrame
us_data = us_data.join(state_loc)
us_data.head()


# #### Create Shapefile Dataframe

# In[103]:


# Store relative path
shapefile = 'Resources\stateshapes\cb_2018_us_state_500k.shp'

# Read shapefile using Geopandas
gdus = gpd.read_file(shapefile)
gdus= gdus.rename(columns={'NAME': 'STATE'})
gdus.head()


# #### Merge DataFrames

# In[104]:


us_data.STATE = us_data.STATE.str.strip() 
gdus.STATE = gdus.STATE.str.strip() 
us_geodata=us_data.merge(gdus, on='STATE', how='left')


# #### Cast to GeoDataFrame

# In[105]:


us_geodata = GeoDataFrame(us_geodata)
type(us_geodata)


# #### Clean GeoDataFrame

# In[106]:


us_geodata.columns


# In[107]:


us_geodata=us_geodata.drop(['STATEFP', 'STATENS',
       'AFFGEOID', 'GEOID', 'LSAD', 'ALAND', 'AWATER'], axis=1)
       
us_geodata=us_geodata.rename(columns= {'STUSPS':'CODE'})


# In[108]:


us_geodata.head()


# In[109]:


us_geodata[us_geodata.isna().any(axis=1)]


# #### Manually Input Code and Shapefile for Washington, DC

# In[110]:


# Copy relative path of .shp file
shapefile = 'Resources\Washington_DC_Boundary\Washington_DC_Boundary.shp'

# Read shapefile using Geopandas
dc_shp = gpd.read_file(shapefile)
dc_shp


# In[111]:


us_geodata.STATE = us_geodata.STATE.str.strip()
us_geodata.set_index('STATE', inplace=True)
us_geodata.at['District Of Columbia','geometry'] = dc_shp.iat[0,9]         # Locate cell and replace with value
us_geodata.at['District Of Columbia','CODE'] = "DC"                        # Locate cell and replace with value


# In[112]:


us_geodata.reset_index(inplace= True)


# In[139]:


usgeoisnull = us_geodata.isnull().any()

#create a subplot without frame
plot = plt.subplot(111, frame_on=False)

#remove axis
plot.xaxis.set_visible(False) 
plot.yaxis.set_visible(False) 

#create the table plot and position it in the upper left corner
table(plot, usgeoisnull,loc='upper right')

#save the plot as a png file
plt.savefig('images/geoisnull.png', bbox_inches = "tight")


# In[114]:


dfi.export(us_geodata, 'images/usgeodata.png', max_rows=10)


# ## GeoMap using Plotly

# In[115]:


fig = px.choropleth(geo_global_data,                                        # Create Choropleth figure with Plotly Express
                    geojson=geo_global_data.geometry,                       # Use geometry for geojson 
                    locations=geo_global_data.COUNTRY,                      # Country names as locations
                    locationmode='country names',                           # Set location mode to recognize country names
                    color="TOTCASES_PER_1M",                                # Numerical values 
                    projection = "natural earth",                           # Map layout
                    width=900, 
                    height=600, 
                    color_continuous_scale="spectral_r",                    # Color scheme
                    title='Total Cases Per Million by Country')

#fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_x=.5)                                               # Center title
fig.show()

fig.write_image('images/totcasechloro.png')


# In[116]:


fig = px.choropleth(geo_global_data, 
                    geojson=geo_global_data.geometry, 
                    locations=geo_global_data.COUNTRY, 
                    locationmode='country names',
                    projection = "natural earth",
                    color="DEATH_PER_1M", 
                    width=900, 
                    height=600, 
                    color_continuous_scale="spectral_r", 
                    title='Total Deaths Per Million by Country')

#fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_x=.5)
fig.show()

fig.write_image('images/totdeathchloro.png')


# In[117]:


px.set_mapbox_access_token("pk.eyJ1Ijoib21rYXJzMSIsImEiOiJja2x3b2VxZGYwZWNtMnVrdnl1aTFhYmoyIn0.y32QE3QdwHh-eoEVBJ5N1Q")

fig = px.scatter_geo(geo_global_data,
                    lat=geo_global_data.LAT,                # Latitutinal values
                    lon=geo_global_data.LONG,               # Longitudinal values
                    hover_name="COUNTRY",                   # Hovering over point will display country
                    projection="natural earth",             # Map type
                    size = 'POPULATION',                    # Numerical value of population determines size of bubble
                    color = 'CONTINENT',                    # Hue
                    width=900, 
                    height=600,
                    size_max = 75,                          # Max size of bubbles
                    title = 'Population by Country',
                    custom_data=["COUNTRY","TOTALCASES","TESTS_PER_1M","SURVIVAL_RATE", "DEATH_RATE", "ACTIVECASES", "GDP_PER_CAPITA"])
                    

fig.update_traces(hovertemplate="<br>".join([
        "COUNTRY: %{customdata[0]}",
        "TOTAL CASES: %{customdata[1]}",
        "TESTS PER MILLION: %{customdata[2]}",
        "SURVIVAL RATE : %{customdata[3]}",
        "DEATH RATE: %{customdata[4]}",
        "ACTIVE CASES: %{customdata[5]}",
        "GDP PER CAPITA: %{customdata[6]}"
    ]))
fig.update_layout(title_x=.5)
fig.show()

fig.write_image('images/countrypopbubble.png')


# ### State Data

# In[118]:


fig = px.choropleth(us_geodata,                                                                     # Create choropleth figure
                    geojson=us_geodata.geometry,                                                    # Polygons for geojson
                    locations=us_geodata.CODE,                                                      # ISO Code
                    color="TOTCASES_PER_1M",                                                        # Numerical measure
                    color_continuous_scale="Viridis",                                               # Color scheme for scale
                    locationmode = "USA-states",                                                    # Will recognize state names as locations
                    scope="usa",                                                                    # Map will only disply United States
                    labels={'TOTCASES_PER_1M':'Total Confirmed Cases Per Million'},                 # Label for scale
                    title= 'Total Confirmed Cases by State',                                        # Plot title
                    width=900,                                                                     # Map width
                    height=600,                                                                     # Map height
                    hover_name="STATE",                                                             # Hover displays state name
                    custom_data=["STATE","TOTCASES_PER_1M","POPULATION"])                           # Included in hover
                    

fig.update_traces(hovertemplate="<br>".join([
        "STATE: %{customdata[0]}",
        "TOTCASES_PER_1M: %{customdata[1]}",
        "POPULATION: %{customdata[2]}"
    ]))

fig.update_layout(title_x=.5)
fig.show()

fig.write_image('images/statetotchloro.png')


# In[119]:


fig = px.choropleth(us_geodata, 
                    geojson=us_geodata.geometry, 
                    locations=us_geodata.CODE, 
                    color="DEATH_PER_1M",
                    color_continuous_scale="Viridis",
                    locationmode = "USA-states",
                    scope="usa",
                    labels={'DEATH_PER_1M':'Deaths per million'},
                    title= 'Deaths Per Million by State',
                    width=900, 
                    height=600,
                    hover_name="STATE",
                    custom_data=["STATE","DEATH_PER_1M","POPULATION"])

fig.update_traces(hovertemplate="<br>".join([
        "STATE: %{customdata[0]}",
        "DEATHS PER MILLION: %{customdata[1]}",
        "POPULATION: %{customdata[2]}"
    ]))

fig.update_layout(title_x=.5)
fig.show() 

fig.write_image('images/statedeathchloro.png')


# In[ ]:




