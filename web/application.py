#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import subprocess as sp
from datetime import datetime
from flask import Flask, render_template, send_from_directory, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_moment import Moment

try:
  from secrets import *
except ImportError:
  sys.exit("Please create a file with a config dictionary in: secrets.py")

# initialization
app = Flask(__name__)

mysql = MySQL(app)
moment = Moment(app)
bootstrap = Bootstrap(app)

app.config.update(
    DEBUG = False,
)

# MySQL configurations
app.config['MYSQL_USER'] = config['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = config['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = 'dbIPRangeMess'
app.config['MYSQL_HOST'] = 'localhost'

#mysql.init_app(app)

# controllers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

def ips():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT INET_NTOA(`ip`) from ipv4s''')
    rv = cur.fetchall()
    return str(rv)

def ipcheck(host):
    status,result = sp.getstatusoutput("ping -c1 -w2 " + str(host))
    if status == 0:
        print("System " + str(host) + " is UP !")
    else:
        print("System " + str(host) + " is DOWN !")

@app.route("/")
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route("/ip")
def ip():
    return render_template('ip.html', current_time=datetime.utcnow())

# launch
if __name__ == "__main__":
    app.run()
