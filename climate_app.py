# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = scoped_session(sessionmaker(bind=engine))



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def paths():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/**Start date in following format:  **yyyy-mm-dd<br/>"
        f"/api/v1.0/**Start date and end date in following format: **yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def percipitation():



    # Query all percipitation and dates for stations
    prcp_date = session.query(Measurement.date, Measurement.prcp).\
    order_by(Measurement.date.asc()).all()
    
    # Convert the query results to a Dictionary using date as the key and prcp as the value
    prcp_date_dict = dict(prcp_date)

    session.close()

    # Return dictionary
    return jsonify(prcp_date_dict)



@app.route("/api/v1.0/stations")
def stations():


    # Query to get a list of all stations
    stations = session.query(Station.station).all()
    
    
    session.close()

  
    # Return stations
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    # Query to get the last year of TOBS and dates
    tobs_obs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date.asc()).all()
    tobs_obs_list = list(np.ravel(tobs_obs))

    
    session.close()

    # Return the TOBS and dates
    return jsonify(tobs_obs_list)



@app.route("/api/v1.0/<start>")
def start(start):


    # Query to get the TOBS info for the start to last date
    start_to_last = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()


    session.close()


    # Return start to last
    return jsonify(start_to_last)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):


    # Query to get the TOBS info for the start and end dates
    start_to_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                   filter(Measurement.date >= start).filter(Measurement.date <= end).all()


    session.close()


    # Return TOBS info for the start through end dates
    return jsonify(start_to_end)


# Run debug for the command line
if __name__ == '__main__':
    app.run(debug=True)
