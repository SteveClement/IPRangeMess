#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import subprocess as sp
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, send_from_directory, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

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

# Flask-WTF Config
app.config['SECRET_KEY'] = 'H4rd t0 gu3ss $tr1ng'

# MySQL configurations
app.config['MYSQL_USER'] = config['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = config['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = 'dbIPRangeMess'
app.config['MYSQL_HOST'] = 'localhost'

#mysql.init_app(app)

# Classes

class NameForm(Form):
  name = StringField('What is your little name?', validators=[Required()])
  submit = SubmitField('Submit')

# controllers

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500

@app.errorhandler(502)
def page_not_found(e):
  return render_template('502.html'), 502

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
  form = NameForm()
  if form.validate_on_submit():
      old_name = session.get('name')
      if old_name is not None and old_name != form.name.data:
          flash('Looks like you have changed your name!')
      session['name'] = form.name.data
      form.name.data = ''
      return redirect(url_for('index'))
  return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

@app.route("/ip")
def ip():
  return render_template('ip.html', current_time=datetime.utcnow())

# launch
if __name__ == "__main__":
  app.run()
