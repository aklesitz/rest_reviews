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
            username VARCHAR(255),
            date date,
            review TEXT
    )
""")

data_tuples = df.itertuples(index = False, name = None)

insert_query = """
    INSERT INTO reviews (username, date, review)
    VALUES (%s, %s, %s)
"""

cur.executemany(insert_query, data_tuples)

conn.commit()

cur.close()
conn.close()
