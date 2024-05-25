# airport_database.py
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('airport_data.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    num_airport INTEGER
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS distances (
                    id INTEGER PRIMARY KEY,
                    city_id INTEGER,
                    airport_id INTEGER,
                    distance FLOAT
                    )''')

# Create an airports table to store airport details
cursor.execute('''CREATE TABLE IF NOT EXISTS airports (
                    AirportID INTEGER PRIMARY KEY,
                    Name TEXT,
                    City TEXT,
                    Country TEXT,
                    IATA TEXT,
                    ICAO TEXT,
                    Latitude REAL,
                    Longitude REAL,
                    Altitude INTEGER,
                    Timezone TEXT,
                    DST TEXT,
                    TzDatabaseTimezone TEXT,
                    Type TEXT,
                    Source TEXT
                    )''')

# Commit changes and close connection
conn.commit()
