#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import subprocess as sp
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from raven.contrib.flask import Sentry
from werkzeug.exceptions import HTTPException, NotFound, BadRequest

try:
  from secrets import *
except ImportError:
  sys.exit("Please create a file with a config dictionary in: secrets.py")

# initialization
app = Flask(__name__)

app.config.update(
  DEBUG = False,
)

# Flask-WTF Config
app.config['SECRET_KEY'] = 'H4rd t0 gu3ss $tr1ng -> Ch4nge M3!!!'

# Flask-SQLAlchemy Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(config['MYSQL_USER'], config['MYSQL_PASSWORD'], config['MYSQL_HOST'], config['MYSQL_DB'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

##sentry = Sentry(app, dsn='<YOUR_DSN>')
moment = Moment(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# Classes

## Forms
class nameForm(Form):
  name = StringField('What is your little name?', validators=[Required()])
  submit = SubmitField('Submit')

class IPForm(Form):
  name = StringField('What IP are you checking?', validators=[Required()])
  submit = SubmitField('Submit')

## SQLAlchemy

class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  users = db.relationship('User', backref='role')

  def __repr__(self):
    return '<Role %r>' % self.name

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

  def __repr__(self):
    return '<User %r>' % self.username

class IPv4s(db.Model):
  __tablename__ = 'ipv4s'
  id = db.Column(db.Integer, primary_key=True)
  ip = db.Column(db.Integer)
  subnet = db.Column(db.SmallInteger)
  hostname = db.Column(db.String(255), nullable=True)
  aliases = db.Column(db.String(255), nullable=True)
  vlan = db.Column(db.SmallInteger, nullable=True)
  services = db.Column(db.Text, nullable=True)
  v6 = db.Column(db.Enum)
  dns = db.Column(db.Enum)
  ptr = db.Column(db.Enum)
  dhcp = db.Column(db.Enum)
  munin = db.Column(db.Enum)
  wiki = db.Column(db.Enum)
  vm = db.Column(db.Enum)
  backup = db.Column(db.Enum)
  mailOut = db.Column(db.Enum)
  syslogOut = db.Column(db.Enum)
  pingeable = db.Column(db.Enum)
  MACs = db.Column(db.Text)
  comments = db.Column(db.Text, nullable=True)
  modifiedTS = db.Column(db.DateTime)
  addedTS = db.Column(db.DateTime)
  deletedTS = db.Column(db.DateTime)
  deleted = db.Column(db.Enum)

  def __repr__(self):
    return '<IPv4s %r>' % self.ip

# controllers

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', current_time=datetime.utcnow()), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html', current_time=datetime.utcnow()), 500

@app.errorhandler(502)
def page_not_found(e):
  return render_template('502.html', current_time=datetime.utcnow()), 502

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

def ips():
  return IPv4s.query.all()

def ipcheck(host):
  status,result = sp.getstatusoutput("ping -c1 -w2 " + str(host))
  if status == 0:
      print("System " + str(host) + " is UP !")
  else:
      print("System " + str(host) + " is DOWN !")

@app.route("/", methods=['GET', 'POST'])
def index():
  form = nForm = nameForm()
  ipForm = IPForm()
  if nForm.validate_on_submit():
      old_name = session.get('name')
      if old_name is not None and old_name != nForm.name.data:
          flash('Looks like you have changed your IP query')
      session['name'] = nForm.name.data
      nForm.name.data = ''
      return redirect(url_for('index'))
  return render_template('index.html', form=nForm, ipForm=IPForm, name=session.get('name'), current_time=datetime.utcnow())

@app.route("/ip")
def ip():
  return render_template('ip.html', ips=ips(), current_time=datetime.utcnow())

# launch
if __name__ == "__main__":
  app.run()
