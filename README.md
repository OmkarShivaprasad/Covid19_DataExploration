# Covid-19 Exploratory Data Analysis
---
Covid-19 is a disease caused by SARS-CoV-2. The World Health Organization declared the disease a pandemic on March 11th, 2020. Since then there have been numerous outlets that have compiled data and presented information pertaining to its spread. Information from Worldometer, a reference website reputed by the American Library Association, will be used as the primary dataset. Worldometer gathers and compiles information from various sources, including government communication channels as well as local media. It provides live updates on the total cases, new cases, total deaths, new deaths,recoveries and critical cases by country, territory or conveyance pertaining to Covid-19.

---

## Overview:
This exploratory analysis will provide a broad level overview of the Covid-19 pandemic. It will contain information from the most recent update on the Worldometer website. Other datasets will be used in order to supplement the information from the Worldometer dataset in order to aid in visualization and geomappiThis analysis will show the steps for data wrangling using Pandas in order to make data ready for visualization, correlation analysis, and geomapping.

---

## Steps in Analysis:
1. Import required libraries

2. Gather data

	- Webscraping with BeautifulSoup and Selenium
	- Reading in CSV files
	- Saving information into Pandas dataframes

3. Clean data

	- Manage null and missing values
	- Drop unwanted rows and columns
	- Rename columns and observations
	- Format datatypes
	- Add columns with calculations
	- Concatenate dataframes

4. Visualization

	- Seaborn | MatPlotLib | Plotly
	- Pearson Correlation Heatmaps
	- Bar Plots
	- Pair Plots
	- Pie Plots
	- Bubble Plots

5. Global GDP Exploration

	- Scatter Plots
	- Pearson Correlation

6. GeoMapping

	- Plotly Library
	- Choropleth
	- ScatterGeo

---

## Data Sources:
- Worldometer Covid-19 Live Information (Countries and US States)
- GDP per Capita (Countries)
- Geospatial Data (Countries and US States)
- Land Size (Countries)

---

## Preview:

### Data Gathering and Cleaning
</br>

#### *Global Data* 
</br>

Global Covid-19 Raw Data

![](images/globaldataraw.png)

Global Covid-19 Initial Clean

![](images/globaldataclean.png)

Global GDP Per Capita Raw Data

![](images/countrygdpraw.png)

Global GDP Per Capita Clean

![](images/countrygdpclean.png)

Country Area Raw Data

![](images/countryarearaw.png)

Country Area Clean

![](images/countryareaclean.png)

Global Data Concatenated with Global GDP Per Capita and Country Area

![](images/globaldataconcat.png)



