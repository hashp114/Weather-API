from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config
from models import db
from resources.weather_resource import WeatherResource
from resources.weather_stats_resource import WeatherStatsResource

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Weather API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Adding resources to API
api.add_resource(WeatherResource, '/api/weather')
api.add_resource(WeatherStatsResource, '/api/weather/stats')

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        "message": "Welcome to the Weather API. Access the API documentation at /swagger"
    })

# Main entry
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
