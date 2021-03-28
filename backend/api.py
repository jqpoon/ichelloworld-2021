from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.row_factory = lambda cursor, row: {'foo': row[0]}
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)

global count
count = 0
@app.route('/button', methods=['GET', 'POST'])
def button():
    if request.method == 'POST':
        global count
        count = count + 1
        return render_template('button.html', ButtonPressed=count)
    
    return render_template('button.html', ButtonPressed=count)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        return render_template('data.html')

    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        user_search = request.form['userinput']

        return render_template('data.html')

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return render_template('data.html', items=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)