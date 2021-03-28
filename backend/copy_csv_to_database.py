import sqlite3
import pandas as pd

# Quick hacky way to load csvs into our database, 
# there's probably a much better way of loading it directly :)
def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.row_factory = lambda cursor, row: {'foo': row[0]}
    return conn

df = pd.read_csv('ramen')

conn = get_db_connection()
df.to_sql("products", conn, if_exists="append")