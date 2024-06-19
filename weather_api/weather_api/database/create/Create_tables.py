# based on file name, I have considered that below codes means station names. codes are derived from file names shared 
# ("USC0011", "Nebraska"),
# ("USC0012", "Iowa"),
# ("USC0013", "Illinois"),
# ("USC0025", "Indiana"),
# ("USC0033", "Ohio")

# an extra unique row_key of MD5 encryption is added to each table, it will act as unique key
# thewre will be no chance of having duplicate data in the table


import psycopg2
from psycopg2 import sql
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_host, db_user, db_password, db_port, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.new_db_name = db_name
        self.conn = None

    def create_database(self):
        try:
            # Connect to the default 'postgres' database to create the new database
            self.conn = psycopg2.connect(host=self.db_host, user=self.db_user, password=self.db_password, port=self.db_port)
            self.conn.autocommit = True
            cur = self.conn.cursor()
            
            # Check if the database exists, and create it if it does not
            cur.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;"), [self.new_db_name])
            exists = cur.fetchone()
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.new_db_name)))
                logging.info(f"Database '{self.new_db_name}' created successfully.")
            else:
                logging.info(f"Database '{self.new_db_name}' already exists.")
            cur.close()
        except Exception as e:
            logging.error(f"Error creating database: {e}")
        finally:
            if self.conn:
                self.conn.close()

    def create_tables(self):
        try:
            # Connect to the newly created database
            self.conn = psycopg2.connect(host=self.db_host, dbname=self.new_db_name, user=self.db_user, password=self.db_password, port=self.db_port)
            cur = self.conn.cursor()

            # SQL commands to create tables with an additional 'row_key' column
            create_tables_sql = """
            CREATE TABLE IF NOT EXISTS weather_stations (
                id SERIAL PRIMARY KEY,
                station_name VARCHAR(50),
                state VARCHAR(50),
                row_key VARCHAR(100) UNIQUE
            );

            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                max_temp INTEGER NOT NULL,
                min_temp INTEGER NOT NULL,
                precipitation INTEGER NOT NULL,
                station_id INTEGER NOT NULL,
                file_name VARCHAR(50) NOT NULL,
                file_load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                row_key VARCHAR(100) UNIQUE, 
                FOREIGN KEY (station_id) REFERENCES weather_stations(id)
            );

            CREATE TABLE IF NOT EXISTS yield_data (
                id SERIAL PRIMARY KEY,
                year INTEGER NOT NULL,
                yield INTEGER NOT NULL,
                file_load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                row_key VARCHAR(100) UNIQUE
            );
            """

            # Execute the SQL command to create tables
            logging.info("Creating tables...")
            cur.execute(create_tables_sql)
            self.conn.commit()
            logging.info("Tables created successfully.")
            cur.close()
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
        finally:
            if self.conn:
                self.conn.close()

# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager(
        db_host="localhost", 
        db_user="postgres", 
        db_password="admin", 
        db_port="5432", 
        db_name="code_challenge_template"
    )
    db_manager.create_database()
    db_manager.create_tables()
