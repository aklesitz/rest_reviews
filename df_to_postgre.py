import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Getting values of environment variables
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')

conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host, port = port)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
            Username VARCHAR(255),
            Date DATE,
            Review TEXT,
            Overall INTEGER,
            Food INTEGER,
            Service INTEGER,
            Ambience INTEGER
    )
""")

data_tuples = df_combined.itertuples(index = False, name = None)

insert_query = """
    INSERT INTO reviews (Username, Date, Review, Overall, Food, Service, Ambience)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cur.executemany(insert_query, data_tuples)

conn.commit()

cur.close()
conn.close()
