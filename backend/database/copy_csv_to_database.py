import sqlite3
import pandas as pd

# Quick hacky way to load csvs into our database, 
# there's probably a much better way of loading it directly :)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.row_factory = lambda cursor, row: {'foo': row[0]}
    return conn

df = pd.read_csv('out.csv')
df['total_price'].astype(int)

conn = get_db_connection()
df.to_sql("products", conn, if_exists="replace")

def clean_price(x):
    x = x.replace('£', '').replace('p', '').replace('.', '')
    return(x)