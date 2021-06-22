# Wrangling Covid-19 Datasets for Use in Python Data Exploration

---
Covid-19 is a disease caused by SARS-CoV-2. The World Health Organization declared the disease a pandemic on March 11th, 2020. Since then there have been numerous outlets that have compiled data and presented information pertaining to its spread. Information from Worldometer, a reference website reputed by the American Library Association, will be used as the primary dataset. Worldometer gathers and compiles information from various sources, including government communication channels as well as local media. It provides live updates on the total cases, new cases, total deaths, new deaths,recoveries and critical cases by country, territory or conveyance pertaining to Covid-19.

---

## Overview:
This data exploration will provide a broad level overview of the Covid-19 pandemic based on the most recently updated information on Worldometer. Datasets from various sources will be gathered using webscraping with BeautifulSoup and Selenium; this data will be stored in Pandas dataframes, and cleaned.  The final dataset will demonstrate its readiness for use in visualization with MatplotLib, Seaborn, and Plotly, linear regression analysis with Statsmodel Summary, and geomapping with Plotly Express. To veiw the project in its entirety, see 'Project Files' below for veiwing options.

---

## Table of Contents:
- [Project Files](#Project-Files)
- [Data Sources](#Data-Sources)
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

## Project Files:
- [Analysis.pdf](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/Analysis.pdf)- Project PDF: ***This is the most user friendly option to veiw the code and outputs of this project. If you are unable to veiw the PDF in GitHub, click 'Download' to save the file to your computer; if you are on a mobile device, click the three horizontal dots (...) to the right of 'Stored with Git LFS', and then click 'Download' to save to your device.***
- [Analysis.ipynb](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/Analysis.ipynb)- Jupyter Notebook
- [Analysis.py](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/Analysis.py)- Source Code and Markdown
- [global_covid_final_data.csv](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/global_covid_final_data.csv)- Final Cleaned Global Dataset
- [us_covid_final_data.csv](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/us_covid_final_data.csv)- Final Cleaned US Dataset
- [Images](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/images)- Folder containing images of plots, cell outputs, and geomaps

---

## Data Sources:
- [Worldometer Covid-19 Live Information (Countries)](https://www.worldometers.info/coronavirus/)
- [Worldometer Covid-19 Live Information (States)](https://www.worldometers.info/coronavirus/country/us/)
- [GDP per Capita (Countries)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/Resources/csvGDP.csv)
- [GDP per Capita (Exported for Manual Update)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/Resources/gdp_entry.csv.csv)
- [GDP per Capita (Countries Manually Updated)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/blob/main/Resources/gdp_entry2.csv.csv)
- [Geospatial Data (States)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/stateshapes)
- [Geospatial Data (Washington D.C)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/Washington_DC_Boundary)
- [Geospatial Data (Countries: Source 1)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/Longitude_Graticules_and_World_Countries_Boundaries-shp)
- [Geospatial Data (Countries: Source 2)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/UIA_World_Countries_Boundaries-shp)
- [Geospatial Data (CarNetherlands)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/CarNetherlands-shp)
- [Geospatial Data (Hong Kong)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/HK-shp)
- [Geospatial Data (Macao)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/Macao-shp)
- [Geospatial Data (Channel Islands)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/Channel-shp)
- [Land Size (States)](https://github.com/OmkarShivaprasad/Covid19_DataExploration/tree/main/Resources/Square%20miles.csv)
- [Land Size (Countries)](https://www.worldometers.info/geography/largest-countries-in-the-world/)
- [Hawaii Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/hawaii/)
- [South Carolina Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/south-carolina/)
- [Indiana Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/indiana/)
- [Wisconsinn Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/wisconsin/)
- [Alabama Carolina Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/alabama/)
- [Louisiana Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/louisiana/)
- [Nebraska Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/nebraska/)
- [Maine Recovered and Active Cases](https://www.worldometers.info/coronavirus/usa/maine/)

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

# PREVIEW

---

## Data Gathering and Cleaning:
</br>

### *GLOBAL DATA* 
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

**FINAL GLOBAL DATASET**

![](images/geoglobaldata.png)

**All Null Values Managed for Final Global Dataset**

![](images/geoglobaldataisnull.png)

</br>

### *UNITED STATES DATA* 
</br>

**United States Raw Dataset**

![](images/usdataraw.png)

**United States Cleaned Dataset**

![](images/usdataclean.png)

**FINAL US DATASET**

![](images/usgeodata.png)

**Null Values Managed for Final US Dataset**

![](images/usdataisnull.png)

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

![](images/popdenscatter.png)

</br>

![](images/totaltestscatter.png)

</br></br>

##### **Pair Plot**

![](images/pair.png)

---

## **StatsModel Summary**

</br>

### *TOTAL CASES PER MILLION VS GDP*

</br>

**With Constant**

![](images/output1.jpg)

**Without Constant**

![](images/output2.jpg)

</br>

![](images/gdpscatter.png)

</br>

### *DEATHS PER MILLION VS GDP*

</br>

**With Constant**

![](images/output3.jpg)

**Without Constant**

![](images/output4.jpg)

</br>

![](images/gdpdeathscatter.png)

</br>

### *TESTS PER MILLION VS GDP*

</br>

**With Constant**

![](images/output5.jpg)

**Without Constant**

![](images/output6.jpg)

</br>

![](images/gdptestscatter.png)

</br>

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






