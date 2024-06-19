import psycopg2
from datetime import datetime
import logging
import hashlib

# Setup logging
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
        if not self.conn:
            self.conn = psycopg2.connect(host=self.db_host, dbname=self.db_name, user=self.db_user, password=self.db_password, port=self.db_port)
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def calculate_and_store_statistics(self):
        # This query calculates the statistics, computes the row_key, and inserts the data
        query = """
        INSERT INTO station_yearly_statistics (station_name, year, avg_max_temp, avg_min_temp, total_precipitation, row_key)
        SELECT station_name, EXTRACT(YEAR FROM date) AS year,
               AVG(max_temp)/10 AS avg_max_temp, AVG(min_temp)/10 AS avg_min_temp,
               SUM(precipitation)/100 AS total_precipitation,
               MD5(CONCAT(station_name, EXTRACT(YEAR FROM date), AVG(max_temp), AVG(min_temp), SUM(precipitation))) AS row_key
        FROM weather_data
        JOIN weather_stations ON weather_data.station_id = weather_stations.id
        WHERE max_temp IS NOT NULL AND min_temp IS NOT NULL AND precipitation IS NOT NULL
        GROUP BY station_name, EXTRACT(YEAR FROM date)
        ON CONFLICT (row_key) DO UPDATE
        SET avg_max_temp = EXCLUDED.avg_max_temp, avg_min_temp = EXCLUDED.avg_min_temp, total_precipitation = EXCLUDED.total_precipitation;
        """
        cur = self.connect()
        try:
            cur.execute(query)
            self.conn.commit()
            logging.info("Yearly statistics calculated and stored successfully.")
        except Exception as e:
            logging.error(f"Error calculating and storing statistics: {e}")
        finally:
            cur.close()
            self.close()

# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager(db_host="localhost", db_user="postgres", db_password="admin", db_name="code_challenge_template")
    db_manager.calculate_and_store_statistics()
