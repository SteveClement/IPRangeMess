import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, Role, Permission


class UserModelTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    Role.insert_roles()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_ping(self):
    u = User()
    db.session.add(u)
    db.session.commit()
    time.sleep(2)
    last_seen_before = u.last_seen
    u.ping()
    self.assertTrue(u.last_seen > last_seen_before)
