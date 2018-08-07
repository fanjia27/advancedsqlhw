from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct


from collections import defaultdict





engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




app = Flask(__name__)

# Welcome page
@app.route("/")
def home():
    return "Homework_Jia"


#Return the JSON representation of your dictionary of the dates and temperature observations from the last year.
@app.route("/api/v1.0/precipitation")
def precipitation():
	last_day = (dt.datetime.strptime('2017-08-01', '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
	last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-01').filter(Measurement.date<'2017-08-01').order_by(Measurement.date).all()
	dct = defaultdict(list)
	for row in last_year:
		dct[row[0]].append(row[1])
	return jsonify(dct)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
	station_names = list(np.ravel(session.query(Station.station).all()))
	return jsonify(station_names) 


# Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def temperature():
	last_year = session.query(Measurement.tobs).filter(Measurement.date>='2016-08-01').filter(Measurement.date<'2017-08-01').order_by(Measurement.date).all()
	temperature_obs = list(np.ravel(last_year))
	return jsonify(temperature_obs)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def calculate_temps_one(start):
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
	results_list = list(np.ravel(results))
	return jsonify(results_list)


@app.route("/api/v1.0/<start>/<end>")
def calculate_temps_two(start, end):
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	results_list = list(np.ravel(results))
	return jsonify(results_list)


if __name__ == "__main__":
    app.run(debug=True)
