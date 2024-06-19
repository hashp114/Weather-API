import psycopg2
from psycopg2 import sql
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_host, db_user, db_password, db_name, db_port):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_port = db_port

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            return conn
        except psycopg2.Error as e:
            logging.error(f"Unable to connect to the database: {e}")
            return None

    def create_station_yearly_statistics_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS station_yearly_statistics (
            id SERIAL PRIMARY KEY,
            station_name VARCHAR(50) NOT NULL,
            year INTEGER NOT NULL,
            avg_max_temp NUMERIC(5, 2),
            avg_min_temp NUMERIC(5, 2),  
            total_precipitation NUMERIC(10, 2), 
            row_key varchar(100) unique
        );
        """
        conn = self.connect()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return

        try:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
                logging.info("Table 'station_yearly_statistics' created successfully.")
        except Exception as e:
            logging.error(f"Error creating table: {e}")
            conn.rollback()
        finally:
            conn.close()

# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager(db_host="localhost", db_user="postgres", db_password="admin", db_name="code_challenge_template", db_port="5432")
    db_manager.create_station_yearly_statistics_table()
