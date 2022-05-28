import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitations")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date 1 year ago
    final_date = dt.date(2017, 8, 23)
    year_ago = final_date - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.prcp, Measurement.date)\
                                        .filter(Measurement.date >= year_ago)\
                                        .filter(Measurement.date < final_date).all()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for precipitation in results:
        precipitations_dict = {}
        precipitations_dict[precipitation.date] = precipitation.prcp
        all_precipitations.append(precipitations_dict)

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the stations
    results = session.query(Station.station).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in results:
        stations_dict = {}
        stations_dict["station"] = station.station
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago
    final_date = dt.date(2017, 8, 23)
    year_ago = final_date - dt.timedelta(days=365)

    # Perform a query to retrieve the tobs from the previous year of the most active station
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
                            .filter(Measurement.date >= year_ago)\
                            .filter(Measurement.date < final_date)\
                            .filter(Measurement.station =="USC00519281").all()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["station"] = tob.station
        tobs_dict["date"] = tob.date
        tobs_dict["tobs"] = tob.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start, end=""):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query to calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of all_start
    all_start = []
    for start in results:
        start_dict = {}
        start_dict["TMIN"] = start[0]
        start_dict["TAVG"] = start[1]
        start_dict["TMAX"] = start[2]
        all_start.append(start_dict)

    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query to calculate TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start)\
                            .filter(Measurement.date <= end).all()
    
     # Create a dictionary from the row data and append to a list of all_start_end
    all_start_end = []
    for start_end in results:
        start_end_dict = {}
        start_end_dict["TMIN"] = start_end[0]
        start_end_dict["TAVG"] = start_end[1]
        start_end_dict["TMAX"] = start_end[2]
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True)

