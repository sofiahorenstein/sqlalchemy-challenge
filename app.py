import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation values between 2016-08-23 and 2017-08-23"""
    # Query all precipitation values
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()

    session.close()

# Create a dictionary from the row data and append to a list of all precipitation values between 2016-08-23 and 2017-08-23
    last_year_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        last_year_prcp.append(prcp_dict)

    return jsonify(last_year_prcp)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations in the dataset"""
    # Query all stations
    results = session.query(Station.station, Station.name, Station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Temperature Observations (tobs) for the previous year"""
    # Query all temperature observations by station 
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()
    
    session.close()
    
    return jsonify(results)

      # Convert list of tuples into normal list
    last_year_tobs = list(np.ravel(results))

    return jsonify(last_year_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range"""
    #input start date format /startdate as YYYY-MM-DD. ex: http://127.0.0.1:5000/api/v1.0/2017-08-21
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= "2017-08-23").all()

    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def range(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range"""
    #input start and end date format /startdate/enddate as YYYY-MM-DD. ex: http://127.0.0.1:5000/api/v1.0/2017-06-14/2017-08-21
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
    
    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)
