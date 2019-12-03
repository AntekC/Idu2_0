from flask import Flask, escape, request, g, jsonify
import sqlite3, json
from flask_cors import CORS
import json
import re

DATABASE = "./Idu2_0/students.db"
app = Flask(__name__)
CORS(app)


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return 'Index Page'

@app.route('/students')
def students():
    return jsonify(query_db('SELECT * FROM students'))
    get_db().close()
        

@app.route('/students/<student_name>')
def student_page(student_name):
    f_name , l_name = re.findall('[A-Z][^A-Z]*', student_name)[0], re.findall('[A-Z][^A-Z]*', student_name)[1]
    the_username = f"{f_name} {l_name}"
    student = query_db(f"SELECT * FROM students WHERE Student_name = ?",[the_username], one=True)
    if student is None:
        return f"No students named {the_username}"
    else:
        return f"Page of student {student['Student_name']}"


if __name__ == '__main__':
    app.run()