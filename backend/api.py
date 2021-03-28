from flask import Flask, render_template, request, redirect, url_for
from werkzeug.exceptions import abort
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.row_factory = lambda cursor, row: {'foo': row[0]}
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('data'), code=307) # Redirect, keeping the POST data alive
    
    # GET method
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # WARNING - SQL INJECTIONS HIGHLY POSSIBLE (some kind of input sanitation needs to happen here)
        user_search = request.form['userinput']
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM products WHERE product_name LIKE \'%' + user_search + '%\'')
        return render_template('data.html', items=items)

    return render_template('data.html', items=[])