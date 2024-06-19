# Weather-API
# Assumptions

Assumption #1
Based on file name, I have considered that below codes means station names. codes are derived from file names shared 
("USC0011", "Nebraska"),
("USC0012", "Iowa"),
("USC0013", "Illinois"),
("USC0025", "Indiana"),
("USC0033", "Ohio")

Assumption #2 an extra unique row_key of MD5 encryption is added to each table, it will act as unique key
there will be no chance of having duplicate data in the table


# Weather API

This is a Flask-based Weather API that provides endpoints for weather data and yearly statistics.

## Setup
cd weather_api
1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Set up the database:

python database\create\Create_tables.py
python database\ingest\load_data.py
``` data has been loaded till here ``

``` now create the statistics table as data mart```
python weather_api\database\data_mart\create\create_statistics_table.py
python weather_api\database\data_mart\ingest\data_analysis.py


3. Run the application:
    ```sh
    python app.py
    ```

4. Run the tests:
    ```sh
    python tests/test_app.py
    ```

## Endpoints

- `GET /api/weather`: Get weather data with pagination and filtering options.
- `GET /api/weather/stats`: Get yearly weather statistics with pagination and filtering options.

http://127.0.0.1:5000/api/weather - weather info
http://127.0.0.1:5000/api/weather/stats - weather stats
## Swagger UI

Access the Swagger UI documentation at `http://localhost:5000/swagger`.
