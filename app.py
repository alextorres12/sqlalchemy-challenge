from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]<br/>"
        f"/api/v1.0/[start]/[end]"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
        filter(Measurement.date > query_date).all()
    session.close()

    all_precipitation = []
    for result in results:
        precepitation_dict = {}
        precepitation_dict[result.date] = result.prcp
        all_precipitation.append(precepitation_dict)

    return jsonify(all_precipitation)


if __name__ == '__main__':
    app.run(debug=True)