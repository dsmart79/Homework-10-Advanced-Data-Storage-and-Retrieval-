import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Climate App<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2017-01-01').all()
        
    all_prcp = []
    for prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = Measurement.date
        prcp_dict["TOBS"] = Measurement.tobs
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()
    
    all_stations = list(np.ravel(station_results))
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date > '2017-01-01').all()
    
    all_tobs = list(np.ravel(tobs_results))
    
    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)