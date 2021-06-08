# Covid-19 Exploratory Data Analysis
---
Covid-19 is a disease caused by SARS-CoV-2. The World Health Organization declared the disease a pandemic on March 11th, 2020. Since then there have been numerous outlets that have compiled data and presented information pertaining to its spread. Information from Worldometer, a reference website reputed by the American Library Association, will be used as the primary dataset. Worldometer gathers and compiles information from various sources, including government communication channels as well as local media. It provides live updates on the total cases, new cases, total deaths, new deaths,recoveries and critical cases by country, territory or conveyance pertaining to Covid-19.

---

## Overview:
This exploratory analysis will provide a broad level overview of the Covid-19 pandemic. It will contain information from the most recent update on the Worldometer website. Other datasets will be used in order to supplement the information from the Worldometer dataset in order to aid in visualization and geomappiThis analysis will show the steps for data wrangling using Pandas in order to make data ready for visualization, correlation analysis, and geomapping.

---

## Table of Contents:

- [Steps in Analysis](#Steps-in-Analysis)
- [Data Sources](#Data-Sources)
- [Data Gathering and Cleaning](#Data-Gathering-and-Cleaning)
  * [Global Data](#Global-Data)
  * [United States Data](#United-States-Data)
- [Visualization](#Visualization)
  * [Bar Subplots](#Bar-Subplots)
  * [Pie Subplots](#Pie-Subplots)
  * [Pearson Correlation Heatmaps](#Pearson-Correlation-Heatmaps)
  * [Bubble Plots](#Bubble-Plots)
  * [Scatter Plots](#Scatter-Plots)
  * [Pair Plot](#Pair-Plot)
- [Geomapping](#Geomapping)
  * [Global Data](#Global-Data)
  * [United States Data](#United-States-Data)



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

## Data Gathering and Cleaning:
</br>

#### *Global Data* 
</br>

**Global Covid-19 Raw Dataset**

![](images/globaldataraw.png)

**Global Covid-19 Initial Cleaned Dataset**

![](images/globaldataclean.png)

**Global GDP Per Capita Raw Dataset**

![](images/countrygdpraw.png)

**Global GDP Per Capita Cleaned Dataset**

![](images/countrygdpclean.png)

**Country Area Raw Dataset**

![](images/countryarearaw.png)

**Country Area Cleaned Dataset**

![](images/countryareaclean.png)

**Global Data Concatenated with Global GDP Per Capita and Country Area**

![](images/globaldataconcat.png)

</br>

#### *United States Data* 
</br>

**United States Raw Dataset**

![](images/usdataraw.png)

**United States Cleaned Dataset**

![](images/usdataclean.png)

</br>

---
## Visualization

</br>

##### **Bar Subplots**

![](images/toptenbarplot.png)

</br>

![](images/contbar.png)

</br></br> 

##### **Pie Subplots**

![](images/pie.png)

</br></br>

##### **Pearson Correlation Heatmaps**

![](images/toptenheat.png)

</br>

![](images/usheat.png)

</br>

![](images/worldpearson.png)

</br></br>

##### **Bubble Plots**

![](images/bubble.png)

</br></br>

##### **Scatter Plots**

![](images/gdpdeathscatter.png)

</br>

![](images/gdpscatter.png)

</br>

![](images/gdptestscatter.png)

</br>

![](images/popdenscatter.png)

</br>

![](images/totaltestscatter.png)

</br></br>

##### **Pair Plot**

![](images/pair.png)

---

## Geomapping

</br>

##### **Bubble Plot Geomap**

![](images/countrypopbubble.png)

</br>

##### **Chloropleth Maps**

![](images/totcasechloro.png)

</br>

![](images/totdeathchloro.png)

</br>

![](images/statetotchloro.png)

</br>

![](images/statedeathchloro.png)






