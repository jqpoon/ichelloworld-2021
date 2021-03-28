from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import time
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
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
@app.route('/button', methods=["GET", "POST"])
def button():
    if request.method == "POST":
        global count
        count = count + 1
        return render_template("button.html", ButtonPressed=count)
    
    return render_template("button.html", ButtonPressed=count)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)