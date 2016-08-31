#!/bin/env python3
import os
from flask import Flask, render_template, send_from_directory, request
from flask_mysqldb import MySQL

# initialization
app = Flask(__name__)

mysql = MySQL(app)

app.config.update(
    DEBUG = False,
)

# controllers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.route("/")
def ips():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT COUNT(*) from ipv4s''')
    rv = cur.fetchall()
    return str(rv)

def index():
    print("app.route /")
    return render_template('index.html')

# launch
if __name__ == "__main__":
    app.run()
