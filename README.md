# sqlalchemy-challenge
Student assignment using sqlalchemy and Flask  to first query and analyze climate data and then deliver query results to a web browser from a local host

## Climate Analysts and Exploration
All of the following analysis was done using SQLAlcheny ORM queries, Pandas and Matplotlib
We used the provided starter notebook and attached hawaii sqlite files to complete the analysis and exploration

## Precipitation Analysis
Using  Jupyter notebook we first found the most recent date in the dataset 
Using that most recent date we got the previous 12 months of precipitation data
We loaded the query results into a Pandas Dataframe sorted it and plotted it

## Station Analysis
We queried the total number of stations in the dataset
We found the most active station by sorting the stations and their observations in descending order
We queried the lowest,highest and average temperatures on the most active station
finally we plotted 12 months of temperature observations (TOBS) data

# Climate APP using Flask
With the initial analysis completed we created an api based on queries we developed.
We used Flask to create our routes

## Routes
Homepage
Preciptation
Stations
Tobs
dynamic start date and static end date for minimum, average and maximum temperatures
dynamic start date and end date for minimum, average and maximum temperatures 


### Resources used
We did use AskBCS to help resolve our code in the app.py file  where we were not able to resolve the end date.
Eventually my instructor Hassan helped me with a small addition to resolve it.
Finally, the app.py and the climate_starter jupyter Source file are in the SurfsUp folder
The Resources folder contains the data source files.

