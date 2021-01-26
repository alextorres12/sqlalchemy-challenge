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
        f"Start Date only: /api/v1.0/YYYY-MM-DD<br/>"
        f"Start and End date: /api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Calculate the date 1 year ago from last data point
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query date and precipation data from that year
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
        filter(Measurement.date > query_date).all()
    session.close()

    # Create dictionary from each row of data and append to a list
    all_precipitation = []
    for result in results:
        precepitation_dict = {}
        precepitation_dict[result.date] = result.prcp
        all_precipitation.append(precepitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name, \
        Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    # Create dictionary from each row of data and append to a list
    all_stations = []
    for result in results:
        station_dict = {}

        station_dict["station"] = result.station
        station_dict["name"] = result.name
        station_dict["latitude"] = result.latitude
        station_dict["longitude"] = result.longitude
        station_dict["elevation"] = result.elevation

        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Get station and date for all readings
    station_count = session.query(Measurement.station, Measurement.date).all()
    station_count_df = pd.DataFrame(station_count)

    # Find the station with the most readings
    grouped_stations = station_count_df.groupby(['station'])
    grouped_stations = grouped_stations.count()
    grouped_stations = grouped_stations.sort_values(["date"], ascending=False)
    grouped_stations = grouped_stations.reset_index(drop=False)

    most_active_station = grouped_stations['station'].iloc[0]

    # Calculate the date 1 year ago from last data point
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the dates and temperature observations of the most active station for the last year
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date > query_date).\
        filter(Measurement.station == most_active_station)

    session.close()

    # Create dictionary from each row of data and append to a list
    all_temps = []
    for result in results:
        temp_dict = {}
        temp_dict["station"] = result.station
        temp_dict["date"] = result.date
        temp_dict["temperature_observed"] = result.tobs

        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def start_date_only(start):
    session = Session(engine)

    # Query dates and temperature observations after a given start date
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start)

    # Save results into a DataFrame
    df = pd.DataFrame(results)

    # Find max, min, and average temperatures
    min_temp = df['tobs'].min()
    max_temp = df['tobs'].max()
    avg_temp = df['tobs'].mean()

    return (
        f"TMIN: {min_temp}<br/>"
        f"TMAX: {max_temp}<br/>"
        f"TAVG: {avg_temp}<br/>"
    )

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    session = Session(engine)

    # Query dates and temperature observations after a given start date
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end)

    # Save results into a DataFrame
    df = pd.DataFrame(results)

    # Find max, min, and average temperatures
    min_temp = df['tobs'].min()
    max_temp = df['tobs'].max()
    avg_temp = df['tobs'].mean()

    return (
        f"TMIN: {min_temp}<br/>"
        f"TMAX: {max_temp}<br/>"
        f"TAVG: {avg_temp}<br/>"
    )

    



if __name__ == '__main__':
    app.run(debug=True)