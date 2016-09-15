# -*- coding: utf-8 -*-
#
from datetime import datetime
import bleach
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from app.exceptions import ValidationError
from . import db

class Permission:
  ADMINISTER = 0x80


class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  default = db.Column(db.Boolean, default=False, index=True)
  permissions = db.Column(db.Integer)
  users = db.relationship('User', backref='role', lazy='dynamic')

  @staticmethod
  def insert_roles():
    roles = {
      'Administrator': (0xff, False)
    }
    for r in roles:
      role = Role.query.filter_by(name=r).first()
      if role is None:
        role = Role(name=r)
      role.permissions = roles[r][1]
      role.default = roles[r][1]
      db.session.add(role)
    db.session.commit()

  def __repr__(self):
    return '<Role %r>' % self.name

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64), unique=True, index=True)
  username = db.Column(db.String(64), unique=True, index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  password_hash = db.Column(db.String(128))
  confirmed = db.Column(db.Boolean, default=True)
  name = db.Column(db.String(64))
  member_since = db.Column(db.DateTime(), default=datetime.utcnow)
  last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

  def __repr__(self):
    return '<User %r>' % self.username

  @staticmethod
  def generate_fake(count=100):
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
      u = User(email=forgery_py.internet.email_address(),
               username=forgery_py.internet.username(True),
               password=forgery_py.lorem_ipsum.word(),
               confirmed=True,
               member_since=forgery_py.date.date(True),
               name=forgery_py.name.full_name())
      db.session.add(u)
      try:
        db.session.commit()
      except IntegrityError:
        db.session.rollback()

    def __init__(self, **kwargs):
      super(User, self).__init__(**kwargs)
      if self.role is None:
        if self.email == current_app.config['IPRM_ADMIN']:
          self.role = Role.query.filter_by(permissions=0xff).first()
        if self.role is None:
          self.role = Role.query.filter_by(default=True).first()


class IPv4s(db.Model):
  __tablename__ = 'ipv4s'
  id = db.Column(db.Integer, primary_key=True)
  ip = db.Column(db.Integer, nullable=False)
  subnet = db.Column(db.SmallInteger, nullable=False)
  hostname = db.Column(db.String(255), nullable=True)
  aliases = db.Column(db.String(255), nullable=True)
  vlan = db.Column(db.SmallInteger, nullable=True)
  services = db.Column(db.Text, nullable=True)
  v6 = db.Column(db.Enum('NO', 'YES'), nullable=False)
  dns = db.Column(db.Enum('NO', 'YES'), nullable=False)
  ptr = db.Column(db.Enum('NO', 'YES'), nullable=False)
  dhcp = db.Column(db.Enum('NO', 'YES'), nullable=False)
  munin = db.Column(db.Enum('NO', 'YES'), nullable=False)
  wiki = db.Column(db.Enum('NO', 'YES'), nullable=False)
  vm = db.Column(db.Enum('NO', 'YES'), nullable=False)
  backup = db.Column(db.Enum('NO', 'YES'), nullable=False)
  mailOut = db.Column(db.Enum('NO', 'YES'), nullable=False)
  syslogOut = db.Column(db.Enum('NO', 'YES'), nullable=False)
  pingeable = db.Column(db.Enum('NO', 'YES'), nullable=False)
  MACs = db.Column(db.Text, nullable=False)
  comments = db.Column(db.Text, nullable=True)
  modifiedTS = db.Column(db.DateTime, nullable=False)
  addedTS = db.Column(db.DateTime, nullable=False)
  deletedTS = db.Column(db.DateTime, nullable=False)
  deleted = db.Column(db.Enum('NO', 'YES'), nullable=False)

  def __repr__(self):
    return '<IPv4s %r>' % self.ip
