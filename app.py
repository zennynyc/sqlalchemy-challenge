import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station


# Create an app
app = Flask(__name__)

# Flask Routes

@app.route("/")
def index():
   return (
      f"Welcome to the Api Assignment!<br/>"
      f"Precipitation: /api/v1.0/precipitation<br/>"
      f"Station list: /api/v1.0/stations<br/>"
      f"Temperature observation: /api/v1.0/tobs<br/>"
      f"/api/v1.0/start<br/>"
      f"/api/v1.0/start:end"
             
   
   )

# Create our session (link) from Python to the DB and query

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    pre_results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all
    session.close()
    for date, prcp in pre_results:
        prep_dict = {}
        prep_dict["date"] = date
        prep_dict["prcp"] = prcp
        prec_q.append(prep_dict)
    return jsonify(prec_q)
 
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    query_station = session.query(distinct(measurement.station)).all()
    session.close()
    station_names = list(np.ravel(query_station))
    return jsonify(station_names)

#Query the dates and temperature observations of the most active station for the last year of data.
  
# Return a JSON list of temperature observations (TOBS) for the previous year.  

@app.route("/api/v1.0/tobs")
def temp():
     session = Session(engine)
     one_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
     temp_query = session.query(measurement.tobs).filter(measurement.date >= one_Year).\
                  filter(measurement.station == 'USC00519281').all()
     temp_list = list(np.ravel(temp_query))
     session.close()
     return jsonify(temp_list)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")
def method1(start):
     session = Session(engine)
     start_date= dt.datetime.strptime(start, '%Y-%m-%d')
     last_year1 = dt.timedelta(days=365)
     start = start_date - last_year1
     end =  dt.date(2017, 8, 23)
     querydata = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
     data = list(np.ravel(querydata))
     return jsonify(data)

#  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def method2(start,end):

     start_date= dt.datetime.strptime(start, '%Y-%m-%d')
     end_date= dt.datetime.strptime(end,'%Y-%m-%d')
     last_year2 = dt.timedelta(days=365)
     start2 = start_date - last_year2
     end = end_date - last_year2
     querydata_2 = session.query(func.min(measurement.tobs),                func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start2).filter(measurement.date <= end).all()
     data_2 = list(np.ravel(querydata_2))
     return jsonify(data_2)
if __name__ == "__main__":
    app.run(debug=True)