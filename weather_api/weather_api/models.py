from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Integer, nullable=False)
    min_temp = db.Column(db.Integer, nullable=False)
    precipitation = db.Column(db.Integer, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('weather_stations.id'), nullable=False)
    file_name = db.Column(db.String(50), nullable=False)
    file_load_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    row_key = db.Column(db.String(100), unique=True)

class WeatherStations(db.Model):
    __tablename__ = 'weather_stations'
    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    row_key = db.Column(db.String(100), unique=True)

# class YieldData(db.Model):
#     __tablename__ = 'yield_data'
#     id = db.Column(db.Integer, primary_key=True)
#     year = db.Column(db.Integer, nullable=False)
#     yield_value = db.Column(db.Integer, nullable=False)
#     row_key = db.Column(db.String(100), unique=True)

class StationYearlyStatistics(db.Model):
    __tablename__ = 'station_yearly_statistics'
    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Numeric(5, 2))
    avg_min_temp = db.Column(db.Numeric(5, 2))
    total_precipitation = db.Column(db.Numeric(10, 2))
    row_key = db.Column(db.String(100), unique=True)
