# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify


#################################################
# Database Setup
#################################################
# Create a connection to database
engine=create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
# From Jupyter Notebook we know there are two tables measurement and station
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def Welcome():
    return (
        f"Available Rountes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature: /api/v1.0/tobs<br/>"
        f"Temperature statistics from start date: /api/v1.0/start<br/>"
        f"Temperature statistics from start date to end date: /api/v1.0/start_end<br/>"
        f"Note: for start date please use the following format: YYYY-mm-dd<br/>"
        f"Note: to access data between start and end date please use the following format: YYYY-mm-dd/YYYY-mm-dd"
    )

#Creating a route that queries precipitation levels and dates and returns a dict using date as key and precipitation as value
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation and date data """

    #Creating a new variable to store results 
    precipitation_query = session.query(Measurement.prcp,Measurement.date).all()

    session.close()

    #Creating a dictionary from the row data and appending to a list precipitation query values

    precipitation_query_values = []
    for prcp, date in precipitation_query:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"]= date
        precipitation_query_values.append(precipitation_dict)

    return jsonify(precipitation_query_values)

#Creating a route that returns a JSON list of stations from db
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the db """

    #Creating a new variable to store results 
    station_query = session.query(Station.station,Station.id).all()

    session.close()

    #Creating a dictionary from the row data and appending to a list precipitation query values

    station_query_values = []
    for station, id in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["id"]= id
        station_query_values.append(station_dict)

    return jsonify(station_query_values)

#Create a query to pull the dates and temperature observations of the most active station for the previous year of data
@app.route("/api/v1.0/tobs")
def tobs():
    #Create a session (link) from Python to the DB
    session = Session(engine)
    lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate=dt.datetime.strptime(lateststr, '%Y-%m-%d')
    startdate= dt.date(latestdate.year - 1, latestdate.month, latestdate.day)
    sel = [Measurement.date,Measurement.tobs]
    queryresult = session.query(*sel).filter(Measurement.date >=startdate).all()
    session.close()

    lastyeartobs = []
    for date, tobs in queryresult:
        tobs_dict ={}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        lastyeartobs.append(tobs_dict)

    return jsonify(lastyeartobs)

#Create a query to pull a dynamic list of tobs values given a chosen start date
@app.route("/api/v1.0/<start>")
def get_start_date(start):
    session = Session(engine)

    minavgmax = session.query((Measurement.date),func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()

    #Creating a dictionary from the row data and appending to a dynamic list of tobs values given start date

    tobsfromstart = []
    for date,min,avg,max in minavgmax:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Min"]= min
        tobs_dict["Avg"]= avg
        tobs_dict["Max"]= max
        tobsfromstart.append(tobs_dict)

    return jsonify(tobsfromstart)
        
#Create a query to pull a dynamic list of tobs values given a chosen start and ending date
@app.route("/api/v1.0/<start>/<end>")
def get_start_end_date(start,end):
    session = Session(engine)

    #select date, min(tobs),avg(tobs),max(tobs) from measurement group by date where date > start and date < end
    minavgmaxstend = session.query((Measurement.date),func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    #Creating a dictionary from the row data and appending to a dynamic list of tobs values given start date and end date

    tobsfromstartend = []
    for date,min,avg,max in minavgmaxstend:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Min"]= min
        tobs_dict["Avg"]= avg
        tobs_dict["Max"]= max
        tobsfromstartend.append(tobs_dict)

    return jsonify(tobsfromstartend)

   

if __name__ == '__main__':
    app.run(debug=True)
    