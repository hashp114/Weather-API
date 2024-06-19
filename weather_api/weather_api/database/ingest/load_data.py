# based on file name, I have considered that below codes means station names. codes are derived from file names shared 
# ("USC0011", "Nebraska"),
# ("USC0012", "Iowa"),
# ("USC0013", "Illinois"),
# ("USC0025", "Indiana"),
# ("USC0033", "Ohio")

import psycopg2
from psycopg2 import sql
import os
import logging
from datetime import datetime
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_host, db_user, db_password, db_name, db_port="5432"):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_port = db_port
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(host=self.db_host, dbname=self.db_name, user=self.db_user, password=self.db_password, port=self.db_port)
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def load_weather_stations(self):
        query = """
        INSERT INTO weather_stations (station_name, state, row_key) VALUES (%s, %s, %s)
        ON CONFLICT (row_key) DO NOTHING;
        """
        stations = [
            ("USC0011", "Nebraska"),
            ("USC0012", "Iowa"),
            ("USC0013", "Illinois"),
            ("USC0025", "Indiana"),
            ("USC0033", "Ohio")
        ]
        cur = self.connect()
        try:
            for station_name, state in stations:
                # Generate row_key as MD5 hash of concatenated station_name and state
                row_key = hashlib.md5(f"{station_name}{state}".encode('utf-8')).hexdigest()
                cur.execute(query, (station_name, state, row_key))
            self.conn.commit()
            logging.info("Weather stations loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading weather stations: {e}")
        finally:
            cur.close()
            self.close()

    def load_yield_data(self, folder_path):
        query = """
        INSERT INTO yield_data (year, yield, row_key) VALUES (%s, %s, %s)
        ON CONFLICT (row_key) DO NOTHING;
        """
        cur = self.connect()
        try:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    for line in file:
                        year, yield_value = map(int, line.split())
                        row_key = hashlib.md5(f"{year}{yield_value}".encode('utf-8')).hexdigest() # Create a unique row_key
                        cur.execute(query, (year, yield_value, row_key))
            self.conn.commit()
            logging.info("Yield data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading yield data: {e}")
        finally:
            cur.close()
            self.close()

    def load_weather_data(self, folder_path):
        query = """
        INSERT INTO weather_data (date, max_temp, min_temp, precipitation, station_id, file_name, row_key)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        """
        cur = self.connect()
        try:
            for file_name in os.listdir(folder_path):
                logging.info(f"Weather data file {file_name} has started loading.")
                station_name = file_name[:7]
                file_path = os.path.join(folder_path, file_name)
                
                cur.execute("SELECT id FROM weather_stations WHERE station_name = %s LIMIT 1;", (station_name,))
                result = cur.fetchone()
                if result is None:
                    logging.warning(f"No station found for station name: {station_name}")
                    continue
                
                station_id = result[0]

                with open(file_path, 'r') as file:
                    for line in file:
                        date_str, max_temp, min_temp, precipitation = line.strip().split()
                        date = datetime.strptime(date_str, '%Y%m%d').date()
                        # Create row_key as MD5 hash of the concatenated fields
                        row_key = hashlib.md5(f"{date}{max_temp}{min_temp}{precipitation}{station_id}{file_name}".encode('utf-8')).hexdigest()
                        cur.execute(query, (date, max_temp, min_temp, precipitation, station_id, file_name, row_key))
                logging.info(f"Weather data file {file_name} has been loaded.")
            self.conn.commit()
            logging.info("Weather data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading weather data: {e}")
        finally:
            cur.close()
            self.close()

if __name__ == "__main__":
    db_manager = DatabaseManager(db_host="localhost", db_user="postgres", db_password="admin", db_name="code_challenge_template")

    logging.info("Starting to load weather stations...")
    db_manager.load_weather_stations()
    logging.info("Weather stations loaded.")

    logging.info("Starting to load yield data...")
    db_manager.load_yield_data("data/yld_data")
    logging.info("Yield data loaded.")

    logging.info("Starting to load weather data...")
    db_manager.load_weather_data("data/wx_data")
    logging.info("Weather data loaded.")
