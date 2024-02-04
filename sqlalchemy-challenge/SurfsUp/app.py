# app.py for Flask
# Bhagya Prasad

# Import the dependencies.

import pandas as pd
import numpy as np
import datetime as dt

# SQL Toolkit and ORM
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask , jsonify


#################################################
# Database Setup
#################################################

#Create an engine for hawaii.sqllite

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#1. to access '/'

@app.route("/")
def welcome():
    return (f"welcome to the API for Hawaaii Climate Analysis <br/>"
           
           f" Currently available routes <br/>"
           
           f"/api/v1.0/precipitation <br/>"
           
           f"/api/v1.0/stations <br/>"
           
           f"/api/v1.0/tobs <br/>
           
           f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
           
           f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
)

#2. to access '/api/v1.0/precipitation'

@app.route("/api/v1.0/precipitation")

def precipitation():
    m_prcp = session.query(Measurement.prcp , Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    prdict = {date : x for date , x in m_prcp}
    return jsonify(prdict)


#3. to access '/api/v1.0/stations'

@app.route("/api/v1.0/stations")

def station():
    result = session.query(Station.station).all()
    st_list = list(np.ravel(result))
    return jsonify (st_list)

#4. to access '/api/v1.0/tobs'


@app.route("/api/v1.0/tobs")

def tobs():
    tobss = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobss))
    return jsonify (tobs_list)

#5. to access '/api/v1.0/<start>/<end>'

@app.route ("/api/v1.0/<start>/<end>")

def temps(start,end):
    findings = session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found =[] 
    for row in findings:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
                       

if __name__ == "__main__":
   app.run(debug=True)
