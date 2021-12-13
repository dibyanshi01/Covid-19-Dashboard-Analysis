# Covid-19-Dashboard-Analysis
In this Project we are Going to Build a Dashboard in which we shows So many Analysis on the COVID_19 with the help of Dataset .For making this we need Some Basic Knowledge about the website Development and Some Basic Knowledge about the Data Analysis .So we are going to make this Project with the help of Dash which is a python framework for building web application.

Now for making Dashboard first we install all the packages through terminal inside the PayCharm , which we are going to use in this Project:-

Install pandas , Here is the command **pip install pandas**

Install plotly , Here is the command **pip install plotly**

Install dash , Here is the command **pip install dash**

For making attractive website we are going to use Bootstrap which is a free and open source CSS framework. For using Bootstrap in the Dash project we have a certain rule to use. First we make a empty list and inside that list we give all the description about the External Stylesheet in a curly bracket.

# Dataset collected from link: https://github.com/CSSEGISandData/COVID-19

# Field description

FIPS: US only. Federal Information Processing Standards code that uniquely identifies counties within the USA.

Admin2: County name. US only.

Province_State: Province, state or dependency name.

Country_Region: Country, region or sovereignty name. The names of locations included on the Website correspond with the official designations used by the U.S. Department of State.

Last Update: MM/DD/YYYY HH:mm:ss (24 hour format, in UTC).

Lat and Long_: Dot locations on the dashboard. All points (except for Australia) shown on the map are based on geographic centroids, and are not representative of a specific address, building or any location at a spatial scale finer than a province/state. Australian dots are located at the centroid of the largest city in each state.

Confirmed: Counts include confirmed and probable (where reported).

Deaths: Counts include confirmed and probable (where reported).

Recovered: Recovered cases are estimates based on local media reports, and state and local reporting when available, and therefore may be substantially lower than the true number. US state-level recovered cases are from COVID Tracking Project. We stopped to maintain the recovered cases (see Issue #3464 and Issue #4465).

Active: Active cases = total cases - total recovered - total deaths. This value is for reference only after we stopped to report the recovered cases (see Issue #4465)

Incident_Rate: Incidence Rate = cases per 100,000 persons.

Case_Fatality_Ratio (%): Case-Fatality Ratio (%) = Number recorded deaths / Number cases.

All cases, deaths, and recoveries reported are based on the date of initial report. Exceptions to this are noted in the "Data Modification" and "Retrospective reporting of (probable) cases and deaths" subsections below.
